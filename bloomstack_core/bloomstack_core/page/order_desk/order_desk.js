/* global Clusterize */
frappe.provide('erpnext.pos');

frappe.pages['order-desk'].refresh = function(wrapper) {
	if (wrapper.pos) {
		wrapper.pos.make_new_order();
	}
}

frappe.pages['order-desk'].on_page_load = function(wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Order Desk'),
		single_column: true
	});

	wrapper.pos = new erpnext.pos.OrderDesk(wrapper);
	window.cur_pos = wrapper.pos;
};

erpnext.pos.OrderDesk = class OrderDesk {
	constructor(wrapper) {
		this.wrapper = $(wrapper).find('.layout-main-section');
		this.page = wrapper.page;

		const assets = [
			'assets/erpnext/js/pos/clusterize.js',
			'assets/erpnext/css/pos.css'
		];

		frappe.require(assets, () => {
			this.make();
		});
	}

	make() {
		return frappe.run_serially([
			() => frappe.dom.freeze(),
			() => {
				this.prepare_dom();
				this.prepare_menu();
				this.set_online_status();
			},
			() => this.make_new_order(),
			() => {
				if(!this.frm.doc.company) {
					this.setup_company()
						.then((company) => {
							this.frm.doc.company = company;
						});
				}
			},
			() => {
				frappe.dom.unfreeze();
			},
		]);
	}

	set_online_status() {
		this.connection_status = false;
		this.page.set_indicator(__("Offline"), "grey");
		frappe.call({
			method: "frappe.handler.ping",
			callback: r => {
				if (r.message) {
					this.connection_status = true;
					this.page.set_indicator(__("Online"), "green");
				}
			}
		});
	}

	prepare_dom() {
		this.wrapper.append(`
			<div class="pos">
				<section class="cart-container">

				</section>
				<section class="item-container">

				</section>
			</div>
		`);
	}

	make_cart() {
		this.cart = new SalesOrderCart({
			frm: this.frm,
			wrapper: this.wrapper.find('.cart-container'),
			events: {
				on_customer_change: (customer) => {
					this.frm.set_value('customer', customer);
				},
				on_order_type_change: (order_type) => {
					this.frm.set_value('order_type', order_type)

					if (order_type == 'Sample') {
						this.frm.set_value('additional_discount_percentage', 100);
						this.frm.doc.items.forEach(item => {
							this.items.events.update_cart(item.item_code, "discount_percentage", 100);
						})
					} else if (order_type == 'Sales') {
						this.frm.set_value('additional_discount_percentage', 0);
						this.frm.doc.items.forEach(item => {
							this.items.events.update_cart(item.item_code, "discount_percentage", 0);
						})
					}
				},
				submit_order: () => {
					this.submit_sales_order()
				},
				on_delivery_date_change: (delivery_date) => {
					this.delivery_date = delivery_date
				},
				on_field_change: (item_code, field, value, batch_no) => {
					this.update_item_in_cart(item_code, field, value, batch_no);
				},
				on_select_change: () => {
					this.set_form_action();
				},
				get_item_details: (item_code) => {
					return this.items.get(item_code);
				},
				update_batched_item: (item) => {
					this.select_batch_and_serial_no(item)
				}
			}
		});

		frappe.ui.form.on('Sales Order', 'selling_price_list', (frm) => {
			if(this.items.items && !this.items.items.length) {
				this.items.reset_items();
			}
		})
	}

	toggle_editing(flag) {
		let disabled;
		if (flag !== undefined) {
			disabled = !flag;
		} else {
			disabled = this.frm.doc.docstatus == 1 ? true: false;
		}
		const pointer_events = disabled ? 'none' : 'inherit';

		this.wrapper.find('input, button, select').prop("disabled", disabled);
		this.wrapper.find('.number-pad-container').toggleClass("hide", disabled);

		this.wrapper.find('.cart-container').css('pointer-events', pointer_events);
		this.wrapper.find('.item-container').css('pointer-events', pointer_events);

		this.page.clear_actions();
	}

	make_items() {
		this.items = new OrderDeskItems({
			wrapper: this.wrapper.find('.item-container'),
			frm: this.frm,
			events: {
				update_cart: (item, field, value) => {
					if (!this.frm.doc.customer) {
						frappe.throw(__('Please select a customer'));
					}
					// check and warn user if a batch item is our of stock.
					const item_details = this.cart.events.get_item_details(item);

					if (item_details.saleable_qty || !item_details.has_batch_no) {
						this.update_item_in_cart(item, field, value);
						this.cart && this.cart.unselect_all();
					} else {
						frappe.confirm(__(`Batch Item ${item_details.item_name} is out of stock, sure you want to add it to cart?`),
							() => {
								this.update_item_in_cart(item, field, value);
								this.cart && this.cart.unselect_all();
							},
							() => {}
						);
					}
				}
			}
		});
	}

	update_item_in_cart(item_code, field='qty', value=1, batch_no) {
		frappe.dom.freeze();
		if(this.cart.exists(item_code, batch_no)) {
			const search_field = batch_no ? 'batch_no' : 'item_code';
			const search_value = batch_no || item_code;
			const item = this.frm.doc.items.find(i => i[search_field] === search_value);
			frappe.flags.hide_serial_batch_dialog = false;

			if (typeof value === 'string' && !in_list(['serial_no', 'batch_no'], field)) {
				// value can be of type '+1' or '-1'
				value = item[field] + flt(value);
			}

			if (field === 'rate' && item) {
				this.frm.doc.ignore_pricing_rule = 1;

				if (value < 0) {
					frappe.show_alert({
						indicator: 'red',
						message: __('Rate amount cannot be less than 0')
					});
					value = 0;
				}
			}

			if(field === 'serial_no') {
				value = item.serial_no + '\n'+ value;
			}

			// if actual_batch_qty and actual_qty if there is only one batch. In such
			// a case, no point showing the dialog
			const show_dialog = item.has_serial_no || item.has_batch_no;

			if (value && show_dialog && field == 'qty' && ((!item.batch_no && item.has_batch_no) ||
				(item.has_serial_no) || (item.actual_batch_qty != item.actual_qty)) ) {
				this.update_item_in_frm(item, field, value);
				this.frm.doc.items.forEach(item_row => {
					this.update_item_in_frm(item_row)
						.then(() => {
							frappe.dom.unfreeze();
							frappe.run_serially([
								() => {
									if (item_row.qty === 0) {
										frappe.model.clear_doc(item_row.doctype, item_row.name);
									}
								},
								() => this.update_cart_data(item_row),
								() => this.post_qty_change(item_row)
							]);
						});
					});
				this.on_close(item);
			} else {
				this.update_item_in_frm(item, field, value)
					.then(() => {
						frappe.dom.unfreeze();
						frappe.run_serially([
							() => {
								let items = this.frm.doc.items.map(item => item.name);
								if (items && items.length > 0 && items.includes(item.name)) {
									this.frm.doc.items.forEach(item_row => {
										// update cart
										this.on_qty_change(item_row);
									});
								} else {
									this.on_qty_change(item);
								}
							},
							() => this.post_qty_change(item)
						]);
					});
			}
			return;
		}

		let args = { item_code: item_code, delivery_date: this.delivery_date || null };
		if (in_list(['serial_no', 'batch_no'], field)) {
			args[field] = value;
		}

		// add to cur_frm
		const item = this.frm.add_child('items', args);
		frappe.flags.hide_serial_batch_dialog = true;

		frappe.run_serially([
			() => {
				return this.frm.script_manager.trigger('item_code', item.doctype, item.name)
					.then(() => {
						this.frm.script_manager.trigger('qty', item.doctype, item.name)
							.then(() => {
								frappe.run_serially([
									() => {
										let items = this.frm.doc.items.map(i => i.name);
										if (items && items.length > 0 && items.includes(item.name)) {
											this.frm.doc.items.forEach(item_row => {
												// update cart
												this.on_qty_change(item_row);
											});
										} else {
											this.on_qty_change(item);
										}
									},
									() => this.post_qty_change(item)
								]);
							});
					});
			},
			() => {
				const show_dialog = item.has_serial_no || item.has_batch_no;

				// if actual_batch_qty and actual_qty if then there is only one batch. In such
				// a case, no point showing the dialog
				if (show_dialog && field == 'qty' && ((!item.batch_no && item.has_batch_no) ||
					(item.has_serial_no) || (item.actual_batch_qty != item.actual_qty)) ) {
					// check has serial no/batch no and update cart
					this.select_batch_and_serial_no(item);
				}
			}
		]);
	}

	on_qty_change(item) {
		if(item.has_batch_no && !item.batch_no){
			this.on_close(item)
			return;
		}
		frappe.run_serially([
			() => this.update_cart_data(item),
		]);
	}

	post_qty_change(item) {
		this.frm.cscript._calculate_taxes_and_totals()
		this.cart.update_taxes_and_totals();
		this.cart.update_grand_total();
		this.cart.update_qty_total();
		this.cart.scroll_to_item(item.item_code);
		this.set_form_action();
	}

	select_batch_and_serial_no(row) {
		frappe.dom.unfreeze();

		erpnext.show_serial_batch_selector(this.frm, row, (success) => {
			const updated_item = this.frm.doc.items.find(item => item.name === success.name)
			if(updated_item){
				this.update_item_in_frm(updated_item)
			}else{
				this.frm.add_child('items',success)
			}
			this.frm.doc.items.forEach(item => {
				this.update_item_in_frm(item)
					.then(() => {
						// update cart
						frappe.run_serially([
							() => {
								if (item.qty === 0) {
									frappe.model.clear_doc(item.doctype, item.name);
								}
							},
							() => this.update_cart_data(item),
							() => this.post_qty_change(item)
						]);
					});
			})
		}, () => {
			this.on_close(row);
		}, true);
	}

	on_close(item) {
		if (item.qty == 0 || (item.has_batch_no && !item.batch_no)) {
			frappe.model.clear_doc(item.doctype, item.name);
		}
		this.post_qty_change(item)
	}

	update_cart_data(item) {
		this.cart.add_item(item);
		frappe.dom.unfreeze();
	}

	update_item_in_frm(item, field, value) {
		if (field == 'qty' && value < 0) {
			frappe.msgprint(__("Quantity must be positive"));
			value = item.qty;
		} else {
			if (in_list(["qty", "serial_no", "batch"], field)) {
				item[field] = value;
				if (field == "serial_no" && value) {
					let serial_nos = value.split("\n");
					item["qty"] = serial_nos.filter(d => {
						return d!=="";
					}).length;
				}
			} else {
				return frappe.model.set_value(item.doctype, item.name, field, value);
			}
		}

		return this.frm.script_manager.trigger('qty', item.doctype, item.name)
			.then(() => {
				if (field === 'qty' && item.qty === 0) {
					frappe.model.clear_doc(item.doctype, item.name);
				}
			})
	}

	submit_sales_order() {
		this.frm.doc.items.forEach((item) => {
			item.delivery_date = this.delivery_date;
		});
		this.frm.savesubmit()
			.then((r) => {
				if (r && r.doc) {
					this.frm.doc.docstatus = r.doc.docstatus;
					frappe.show_alert({
						indicator: 'green',
						message: __(`Sales Order ${r.doc.name} created succesfully`)
					});

					this.toggle_editing();
					this.set_form_action();
					this.set_primary_action_in_modal();
				}
			});
	}

	set_primary_action_in_modal() {
		if (!this.frm.msgbox) {
			this.frm.msgbox = frappe.msgprint(
				`<a class="btn btn-primary" onclick="cur_frm.print_preview.printit(true)" style="margin-right: 5px;">
					${__('Print')}</a>
				<a class="btn btn-default">
					${__('New')}</a>`
			);

			$(this.frm.msgbox.body).find('.btn-default').on('click', () => {
				this.frm.msgbox.hide();
				this.make_new_order();
			})
		}
	}

	setup_company() {
		return new Promise(resolve => {
			if(!this.frm.doc.company) {
				frappe.prompt({fieldname:"company", options: "Company", fieldtype:"Link",
					label: __("Select Company"), reqd: 1}, (data) => {
						this.company = data.company;
						resolve(this.company);
				}, __("Select Company"));
			} else {
				resolve();
			}
		})
	}

	make_new_order() {
		return frappe.run_serially([
			() => this.make_sales_order_frm(),
			() => {
				if (this.cart) {
					this.cart.frm = this.frm;
					this.cart.reset();
				} else {
					this.make_items();
					this.make_cart();
				}
				this.toggle_editing(true);
			},
		]);
	}

	reset_cart() {
		this.cart.frm = this.frm;
		this.cart.reset();
		this.items.reset_search_field();
	}

	make_sales_order_frm() {
		const doctype = 'Sales Order';
		return new Promise(resolve => {
			if (this.frm) {
				this.frm = get_frm(this.frm);
				if(this.company) {
					this.frm.doc.company = this.company;
				}

				resolve();
			} else {
				frappe.model.with_doctype(doctype, () => {
					this.frm = get_frm();
					resolve();
				});
			}
		});

		function get_frm(_frm) {
			const page = $('<div>');
			const frm = _frm || new frappe.ui.form.Form(doctype, page, false);
			const name = frappe.model.make_new_doc_and_get_name(doctype, true);
			frm.refresh(name);
			frm.doc.items = [];
			frm.doc.is_pos = 1;

			return frm;
		}
	}


	prepare_menu() {
		var me = this;
		this.page.clear_menu();

		this.page.add_menu_item(__("Form View"), function () {
			frappe.model.sync(me.frm.doc);
			frappe.set_route("Form", me.frm.doc.doctype, me.frm.doc.name);
		});
	}

	set_form_action() {
		if(this.frm.doc.docstatus == 1) {
			this.page.set_secondary_action(__("Print"), async() => {
				if(this.frm.doc.docstatus != 1 ){
					await this.frm.save();
				}
				this.frm.print_preview.printit(true);
			});
		}

		if(this.frm.doc.items.length == 0){
			this.page.clear_secondary_action();
		}

		if (this.frm.doc.docstatus == 1) {
			this.page.set_primary_action(__("New"), () => {
				this.make_new_order();
			});
			this.page.add_menu_item(__("Email"), () => {
				this.frm.email_doc();
			});
		}
	}
};

class OrderDeskItems {
	constructor({wrapper, frm, events}) {
		this.wrapper = wrapper;
		this.frm = frm;
		this.items = {};
		this.events = events;
		this.currency = this.frm.doc.currency;

		frappe.db.get_value("Item Group", {lft: 1, is_group: 1}, "name", (r) => {
			this.parent_item_group = r.name;
			this.make_dom();
			this.make_fields();

			this.init_clusterize();
			this.bind_events();
			this.load_items_data();
		})
	}

	load_items_data() {
		// bootstrap with 20 items
		this.get_items()
			.then(({ items }) => {
				this.all_items = items;
				this.items = items;
				this.render_items(items);
			});
	}

	reset_items() {
		this.wrapper.find('.pos-items').empty();
		this.init_clusterize();
		this.load_items_data();
	}

	make_dom() {
		this.wrapper.html(`
			<div class="fields">
				<div class="search-field">
				</div>
				<div class="item-group-field">
				</div>
			</div>
			<div class="items-wrapper">
			</div>
		`);

		this.items_wrapper = this.wrapper.find('.items-wrapper');
		this.items_wrapper.append(`
			<div class="list-item-table pos-items-wrapper">
				<div class="pos-items image-view-container">
				</div>
			</div>
		`);
	}

	make_fields() {
		// Search field
		const me = this;
		this.search_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Data',
				label: __('Search Item (Ctrl + i)'),
				placeholder: __('Search by item code, serial number, batch no or barcode')
			},
			parent: this.wrapper.find('.search-field'),
			render_input: true,
		});

		frappe.ui.keys.on('ctrl+i', () => {
			this.search_field.set_focus();
		});

		this.search_field.$input.on('input', (e) => {
			clearTimeout(this.last_search);
			this.last_search = setTimeout(() => {
				const search_term = e.target.value;
				const item_group = this.item_group_field ?
					this.item_group_field.get_value() : '';

				this.filter_items({ search_term:search_term,  item_group: item_group});
			}, 300);
		});

		this.item_group_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Link',
				label: 'Item Group',
				options: 'Item Group',
				default: me.parent_item_group,
				onchange: () => {
					const item_group = this.item_group_field.get_value();
					this.filter_items({ item_group });
				},
				get_query: () => {
					return {
						query: 'bloomstack_core.bloomstack_core.page.order_desk.order_desk.item_group_query'
					};
				}
			},
			parent: this.wrapper.find('.item-group-field'),
			render_input: true
		});
	}

	init_clusterize() {
		this.clusterize = new Clusterize({
			scrollElem: this.wrapper.find('.pos-items-wrapper')[0],
			contentElem: this.wrapper.find('.pos-items')[0],
			rows_in_block: 6
		});
	}

	render_items(items) {
		let _items = items || this.items;

		const all_items = Object.values(_items).map(item => this.get_item_html(item));
		let row_items = [];

		const row_container = '<div class="image-view-row">';
		let curr_row = row_container;

		for (let i=0; i < all_items.length; i++) {
			// wrap 4 items in a div to emulate
			// a row for clusterize
			if(i % 3 === 0 && i !== 0) {
				curr_row += '</div>';
				row_items.push(curr_row);
				curr_row = row_container;
			}
			curr_row += all_items[i];

			if(i == all_items.length - 1) {
				row_items.push(curr_row);
			}
		}

		this.clusterize.update(row_items);
	}

	filter_items({ search_term='', item_group=this.parent_item_group }={}) {
		if (search_term) {
			search_term = search_term.toLowerCase();

			// memoize
			this.search_index = this.search_index || {};
			if (this.search_index[search_term]) {
				const items = this.search_index[search_term];
				this.items = items;
				this.render_items(items);
				this.set_item_in_the_cart(items);
				return;
			}
		} else if (item_group == this.parent_item_group) {
			this.items = this.all_items;
			return this.render_items(this.all_items);
		}

		this.get_items({search_value: search_term, item_group })
			.then(({ items, serial_no, batch_no, barcode }) => {
				if (search_term && !barcode) {
					this.search_index[search_term] = items;
				}

				this.items = items;
				this.render_items(items);
				this.set_item_in_the_cart(items, serial_no, batch_no, barcode);
			});
	}

	set_item_in_the_cart(items, serial_no, batch_no, barcode) {
		if (serial_no) {
			this.events.update_cart(items[0].item_code,
				'serial_no', serial_no);
			this.reset_search_field();
			return;
		}

		if (batch_no) {
			this.events.update_cart(items[0].item_code,
				'batch_no', batch_no);
			this.reset_search_field();
			return;
		}

		if (items.length === 1 && (serial_no || batch_no || barcode)) {
			this.events.update_cart(items[0].item_code,
				'qty', '+1');
			this.reset_search_field();
		}
	}

	reset_search_field() {
		this.search_field.set_value('');
		this.search_field.$input.trigger("input");
	}

	bind_events() {
		var me = this;
		this.wrapper.on('click', '.pos-item-wrapper', function() {
			const $item = $(this);
			const item_code = unescape($item.attr('data-item-code'));
			me.events.update_cart(item_code, 'qty', '+1');
		});
	}

	get(item_code) {
		let item = {};
		this.items.map(data => {
			if (data.item_code === item_code) {
				item = data;
			}
		})

		return item
	}

	get_all() {
		return this.items;
	}

	get_item_html(item) {
		const price_list_rate = format_currency(item.price_list_rate, this.currency);
		const item_qty_display = item.saleable_qty > 0 ? `Stock: ${item.saleable_qty} ${item.stock_uom}` : "Out of Stock"
		const { item_code, item_name, item_image,item_group} = item;
		const item_title = item_name || item_code;

		const template = `
			<div class="pos-item-wrapper image-view-item" data-item-code="${escape(item_code)}">
				<div class="image-view-header">
					<div>
						<a class="grey list-id ellipsis" data-name="${item_code}" title="${item_title}">
							${item_title},
							<br>
							<span style="font-size: large">
								${item_group}
							<span>
						</a>
					</div>
				</div>
				<div class="image-view-body">
					<a	data-item-code="${item_code}"
						title="${item_title}"
					>
						<div class="image-field"
							style="${!item_image ? 'background-color: #fafbfc;' : ''} border: 0px;"
						>
							${!item_image ? `<span class="placeholder-text">
									${frappe.get_abbr(item_title)}
								</span>` : '' }
							${item_image ? `<img src="${item_image}" alt="${item_title}">` : '' }
						</div>
						<span class="price-info">
							${price_list_rate}
						</span>
						<span class="price-info">
							${item_qty_display}
						</span>
					</a>
				</div>
			</div>
		`;

		return template;
	}

	get_items({start = 0, page_length = 40, search_value='', item_group=this.parent_item_group}={}) {
		const price_list = this.frm.doc.selling_price_list;
		return new Promise(res => {
					frappe.call({
						method: "bloomstack_core.bloomstack_core.page.order_desk.order_desk.get_items",
						freeze: true,
						args: {
							start,
							page_length,
							price_list,
							item_group,
							search_value
						}
					}).then(r => {
						res(r.message);
					});
		});
	}
}

class SalesOrderCart {
	constructor({frm, wrapper, events}) {
		this.frm = frm;
		this.item_data = {};
		this.wrapper = wrapper;
		this.events = events;
		this.make();
		this.bind_events();
	}

	make() {
		this.make_dom();
		this.make_customer_field();
		this.make_order_type_field();
		this.make_delivery_date_field();
	}

	make_dom() {
		this.wrapper.append(`
			<div class="pos-cart">
				<div class="customer-field">
				</div>
				<div class="cart-wrapper table-responsive">
					<table class="table">
					<thead>
						<tr class="table-head">
							<th width="25%">${__('Item Name')}</th>
							<th width="25%">${__('Batch No.')}</th>
							<th>${__('Quantity')}</th>
							<th>${__('Discount')}</th>
							<th>${__('Rate')}</th>
							<th width="7%"></th>
						</tr>
						</thead>
						<tbody class="cart-items">
								<tr class="empty-state">
									<td colspan="6">
										<span>${__('No Items added to cart')}</span>
									</td>
								</tr>
						</tbody>
						<tfoot>
							<tr class="taxes-and-totals">
								${this.get_taxes_and_totals()}
							</tr>
							<tr class="discount-amount">
								${this.get_discount_amount()}
							</tr>
							<tr class="grand-total">
								${this.get_grand_total()}
							</tr>
							<tr class="quantity-total">
								${this.get_item_qty_total()}
							</tr>
					</tfoot>
					</table>
				</div>
				<div class="row">
					<div class="number-pad-container col-sm-6"></div>
				</div>
				<div class="row">
					<div class="submit-order">
						<div class="list-item__content text-muted"></div>
						<div class="list-item__content list-item__content--flex-2">
							<button class="order-primary" type="submit" data-action="submit_order"> Order </button>
						</div>
					</div>
				</div>
			</div>
		`);

		this.$cart_items = this.wrapper.find('.cart-items');
		this.$empty_state = this.wrapper.find('.cart-items .empty-state');
		this.$taxes_and_totals = this.wrapper.find('.taxes-and-totals');
		this.$discount_amount = this.wrapper.find('.discount-amount');
		this.$grand_total = this.wrapper.find('.grand-total');
		this.$qty_total = this.wrapper.find('.quantity-total');
		this.$submit_order = this.wrapper.find('.submit-order');

		this.toggle_taxes_and_totals(false);
		this.$grand_total.on('click', () => {
			this.toggle_taxes_and_totals();
		});
	}

	reset() {
		this.$cart_items.find('.item').remove();
		this.$empty_state.show();
		this.$taxes_and_totals.html(this.get_taxes_and_totals());
		this.customer_field.set_value("");
		this.frm.msgbox = "";

		let total_item_qty = 0.0;
		// hiiremovethis  this.frm.set_value("pos_total_qty",total_item_qty);

		this.$discount_amount.find('input:text').val('');
		this.wrapper.find('.grand-total-value').text(
			format_currency(this.frm.doc.grand_total, this.frm.currency));
		this.wrapper.find('.rounded-total-value').text(
			format_currency(this.frm.doc.rounded_total, this.frm.currency));
		this.$qty_total.find(".quantity-total").text(total_item_qty);

		const customer = this.frm.doc.customer;
		this.customer_field.set_value(customer);
	}

	get_grand_total() {
		let total = this.get_total_template('Grand Total', 'grand-total-value');

		if (!cint(frappe.sys_defaults.disable_rounded_total)) {
			total += this.get_total_template('Rounded Total', 'rounded-total-value');
		}

		return total;
	}

	get_item_qty_total() {
		let total = this.get_total_template('Total Qty', 'quantity-total');
		return total;
	}

	get_total_template(label, class_name) {
		return `
				<td colspan = "3">${__(label)}</td>
				<td colspan = "3" class="${class_name} text-right">0.00</td>
		`;
	}

	get_discount_amount() {
		const get_currency_symbol = window.get_currency_symbol;
		return `
			<td colspan="6">
				<div class="list-item">
					<div class="list-item__content list-item__content--flex-2 text-muted">${__('Discount')}</div>
					<div class="list-item__content discount-inputs">
						<input type="text" class="form-control additional_discount_percentage text-right" placeholder="% 0.00">
						<input type="text" class="form-control discount_amount text-right" placeholder="${get_currency_symbol(this.frm.doc.currency)} 0.00">
				</div>
			</td>
		`;
	}

	get_taxes_and_totals() {
		return `
		<td colspan="6">
			<div class="list-item">
				<div class="list-item__content list-item__content--flex-2 text-muted">${__('Net Total')}</div>
				<div class="list-item__content net-total">0.00</div>
			</div>
			<div class="list-item">
				<div class="list-item__content list-item__content--flex-2 text-muted">${__('Taxes')}</div>
				<div class="list-item__content taxes">0.00</div>
			</div>
			</td>
		`;
	}

	toggle_taxes_and_totals(flag) {
		if (flag !== undefined) {
			this.tax_area_is_shown = flag;
		} else {
			this.tax_area_is_shown = !this.tax_area_is_shown;
		}

		this.$taxes_and_totals.toggle(this.tax_area_is_shown);
		this.$discount_amount.toggle(this.tax_area_is_shown);
	}

	update_taxes_and_totals() {
		if (!this.frm.doc.taxes) { return; }

		const currency = this.frm.doc.currency;
		this.frm.refresh_field('taxes');

		// Update totals
		this.$taxes_and_totals.find('.net-total')
			.html(format_currency(this.frm.doc.total, currency));

		// Update taxes
		const taxes_html = this.frm.doc.taxes.map(tax => {
			return `
				<div>
					<span>${tax.description}</span>
					<span class="text-right bold">
						${format_currency(tax.tax_amount, currency)}
					</span>
				</div>
			`;
		}).join("");
		this.$taxes_and_totals.find('.taxes').html(taxes_html);
	}

	update_grand_total() {
		this.$grand_total.find('.grand-total-value').text(
			format_currency(this.frm.doc.grand_total, this.frm.currency)
		);

		this.$grand_total.find('.rounded-total-value').text(
			format_currency(this.frm.doc.rounded_total, this.frm.currency)
		);
	}

	update_qty_total() {
		var total_item_qty = 0;
		$.each(this.frm.doc["items"] || [], function (i, d) {
				if (d.qty > 0) {
					total_item_qty += d.qty;
				}
		});
		this.$qty_total.find('.quantity-total').text(total_item_qty);
		// hiiremovethis this.frm.set_value("pos_total_qty",total_item_qty);
	}

	make_order_type_field() {
		this.order_type_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Select',
				label: 'Order Type',
				fieldname: 'order_type',
				options: this.frm.get_field("order_type").df.options,
				reqd: 1,
				default: this.frm.doc.order_type,
				onchange: () => {
					this.events.on_order_type_change(this.order_type_field.get_value());
				}
			},
			parent: this.wrapper.find('.customer-field'),
			render_input: true
		});
	}

	make_delivery_date_field() {
		this.delivery_date_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Date',
				label: 'Expected Delivery Date',
				fieldname: 'delivery_date',
				reqd: 1,
				onchange: () => {
					this.events.on_delivery_date_change(this.delivery_date_field.get_value());
				}
			},
			parent: this.wrapper.find('.customer-field'),
			render_input: true
		});
	}

	make_customer_field() {
		this.customer_field = frappe.ui.form.make_control({
			df: {
				fieldtype: 'Link',
				label: 'Customer',
				fieldname: 'customer',
				options: 'Customer',
				reqd: 1,
				get_query: function() {
					return {
						query: 'erpnext.controllers.queries.customer_query'
					}
				},
				onchange: () => {
					this.events.on_customer_change(this.customer_field.get_value());
				}
			},
			parent: this.wrapper.find('.customer-field'),
			render_input: true
		});
		this.customer_field.set_value(this.frm.doc.customer);
	}

	add_item(item) {
		this.$empty_state.hide();
		if (this.exists(item.item_code, item.batch_no)) {
			// update quantity
			this.update_item(item);
		} else if (flt(item.qty) > 0.0) {
			// add to cart
			const $item = $(this.get_item_html(item));
			$item.appendTo(this.$cart_items);
		}
		this.highlight_item(item.item_code);
	}

	update_item(item) {
		const item_selector = item.batch_no ?
			`[data-batch-no="${item.batch_no}"]` : `[data-item-code="${escape(item.item_code)}"]`;

		const $item = this.$cart_items.find(item_selector);

		if(item.qty > 0) {
			const is_stock_item = this.get_item_details(item.item_code).is_stock_item;
			const saleable_qty = this.get_item_details(item.item_code).saleable_qty;
			const indicator_class = (!is_stock_item || saleable_qty >= item.qty) ? 'green' : 'red';
			const remove_class = indicator_class == 'green' ? 'red' : 'green';
			$item.find('.quantity input').val(item.qty);
			$item.find('.discount').text(item.discount_percentage + '%');
			$item.find('.rate input').val(item.rate);
			$item.children('.item').addClass(indicator_class);
			$item.children('.item').removeClass(remove_class);
		} else { 
			$item.remove();
		}
	}

	get_item_html(item) {
		const is_stock_item = this.get_item_details(item.item_code).is_stock_item;
		const saleable_qty = this.get_item_details(item.item_code).saleable_qty;
		const indicator_class = (!is_stock_item || saleable_qty >= item.qty) ? 'green' : 'red';
		const batch_no = item.batch_no || '';

		const me = this;
		$(document).on('click', '.action a', function (event) {
			event.stopImmediatePropagation(); // to prevent firing of multiple events
			let item_name = $(this).data('name');
			let item_code = $(this).data('item-code');
			let total_quantity;
			frappe.confirm(__(`Are you sure you want to remove ${item_name} from the order?`),
				 () => {
					me.events.on_field_change(item_code, 'qty', 0);
					me.update_qty_total();
				}
				);
				
				setTimeout( () => {
					total_quantity = me.$qty_total.find('.quantity-total').text();
					console.log(total_quantity);
					if(total_quantity == 0) {
						me.wrapper.find('.cart-items .empty-state').show();
					}
				}, 1500)
		})

		$(document).on('click', '.list-item div', function (event) {
			event.stopImmediatePropagation(); // to prevent firing of multiple events
			let item_code = $(this).data('item-code');
			if (item_code) {
				const item_data = me.frm.doc.items.find(item => item.item_code === item_code)
				const show_dialog = item_data.has_batch_no;
				if (show_dialog) {
					me.events.update_batched_item(item_data)
				}
			}
		})

		return `
			<tr class="item" data-item-code="${escape(item.item_code)}" data-batch-no="${batch_no}" title="Item: ${item.item_name}  Available Qty: ${saleable_qty || 0} ${item.stock_uom}">
				<td width: 50px class="item-name ellipsis indicator ${indicator_class}" data-item-code="${item.item_code}">
					${item.item_name}
				</td>
				<td class="batch text-center" data-item-code="${item.item_code}">
					${item.batch_no || "-"}
				</td>
				<td class="quantity" data-item-code="${item.item_code}">
					${get_quantity_html(item.qty)}
				</td>
				<td class="discount text-right" data-item-code="${item.item_code}">
					${item.discount_percentage}%
				</td>
				<td class="rate" data-item-code="${item.item_code}">
					${get_rate_html(item.rate)}
				</td>
				<td width: 10px class="action action_button" data-item-code="${item.item_code}">
					<a class="btn btn-danger btn-xs" title="Delete" data-name="${item.item_name}" data-item-code="${item.item_code}">X</a>
				</td>
			</tr>
		`;

		function get_quantity_html(value) {
			return `
				<div class="input-group input-group-xs">
					<input class="form-control" type="number" value="${value}">
				</div>
			`;
		};

		function get_rate_html(rate){
			return `
			<div class="input-group input-group-xs">
				<input class="form-control" type="number" value="${rate}">
			</div>`
		}
	}

	get_item_details(item_code) {
		if (!this.item_data[item_code]) {
			this.item_data[item_code] = this.events.get_item_details(item_code);
		}

		return this.item_data[item_code];
	}

	exists(item_code, batch_no) {
		const is_exists = batch_no ?
			`[data-batch-no="${batch_no}"]` : `[data-item-code="${escape(item_code)}"]`;

		let $item = this.$cart_items.find(is_exists);

		return $item.length > 0;
	}

	highlight_item(item_code) {
		const $item = this.$cart_items.find(`[data-item-code="${escape(item_code)}"]`);
		$item.addClass('highlight');
		setTimeout(() => $item.removeClass('highlight'), 1000);
	}

	scroll_to_item(item_code) {
		const $item = this.$cart_items.find(`[data-item-code="${escape(item_code)}"]`);
		if ($item.length === 0) return;
		const scrollTop = $item.offset().top - this.$cart_items.offset().top + this.$cart_items.scrollTop();
		this.$cart_items.animate({ scrollTop });
	}

	bind_events() {
		const me = this;
		const events = this.events;

		// quantity change
		this.$cart_items.on('click',
			'[data-action="increment"], [data-action="decrement"]', function() {
				const $btn = $(this);
				const $item = $btn.closest('.item[data-item-code]');
				const item_code = unescape($item.attr('data-item-code'));
				const action = $btn.attr('data-action');

				if(action === 'increment') {
					events.on_field_change(item_code, 'qty', '+1');
				} else if(action === 'decrement') {
					events.on_field_change(item_code, 'qty', '-1');
				}
			});

		this.$cart_items.on('click',
			'[data-action="increment_rate"], [data-action="decrement_rate"]', function() {
				const $btn = $(this);
				const $item = $btn.closest('.item[data-item-code]');
				const item_code = unescape($item.data('item-code'));
				const action = $btn.data('action');

				if (action === 'increment_rate') {
					events.on_field_change(item_code, 'rate', '+1');
				} else if (action === 'decrement_rate') {
					events.on_field_change(item_code, 'rate', '-1');
				}
			});

		this.$cart_items.on('change', '.quantity input', function() {
			const $input = $(this);
			const $item = $input.closest('.item[data-item-code]');
			const item_code = unescape($item.attr('data-item-code'));
			events.on_field_change(item_code, 'qty', flt($input.val()));
		});

		this.$submit_order.on('click', '[data-action="submit_order"]',() => {
			events.submit_order()
		})

		this.$cart_items.on('change', '.rate input', function() {
			const $input = $(this);
			const $item = $input.closest('.item[data-item-code]');
			const item_code = unescape($item.data('item-code'));
			events.on_field_change(item_code, 'rate', flt($input.val()));
		});

		// current item
		this.$cart_items.on('click', '.item', function() {
			me.set_selected_item($(this));
		});

		this.wrapper.find('.additional_discount_percentage').on('change', (e) => {
			const discount_percentage = flt(e.target.value,
				precision("additional_discount_percentage"));

			frappe.model.set_value(this.frm.doctype, this.frm.docname,
				'additional_discount_percentage', discount_percentage)
				.then(() => {
					let discount_wrapper = this.wrapper.find('.discount_amount');
					discount_wrapper.val(flt(this.frm.doc.discount_amount,
						precision('discount_amount')));
					discount_wrapper.trigger('change');
				});
		});

		this.wrapper.find('.discount_amount').on('change', (e) => {
			const discount_amount = flt(e.target.value, precision('discount_amount'));
			frappe.model.set_value(this.frm.doctype, this.frm.docname,
				'discount_amount', discount_amount);
			this.frm.trigger('discount_amount')
				.then(() => {
					this.update_discount_fields();
					this.update_taxes_and_totals();
					this.update_grand_total();
				});
		});
	}

	update_discount_fields() {
		let discount_wrapper = this.wrapper.find('.additional_discount_percentage');
		let discount_amt_wrapper = this.wrapper.find('.discount_amount');
		discount_wrapper.val(flt(this.frm.doc.additional_discount_percentage,
			precision('additional_discount_percentage')));
		discount_amt_wrapper.val(flt(this.frm.doc.discount_amount,
			precision('discount_amount')));
	}

	set_selected_item($item) {
		this.selected_item = $item;
		this.$cart_items.find('.item').removeClass('current-item qty disc rate');
		this.selected_item.addClass('current-item');
		this.events.on_select_change();
	}

	unselect_all() {
		this.$cart_items.find('.item').removeClass('current-item qty disc rate');
		this.selected_item = null;
		this.events.on_select_change();
	}
}
