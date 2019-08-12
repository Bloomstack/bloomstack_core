/* global frappe, bloomstack */
frappe.provide("bloomstack.track_and_trace");

{% include "bloomstack_core/bloomstack_core/page/track_and_trace/modules.js" %}

bloomstack.track_and_trace.modules = new bloomstack.track_and_trace.ModulesManager();

{% include "bloomstack_core/bloomstack_core/page/track_and_trace/modules/index.js" %}
{% include "bloomstack_core/bloomstack_core/page/track_and_trace/templates/track_and_trace_main.html" %}
{% include "bloomstack_core/bloomstack_core/page/track_and_trace/templates/track_and_trace_pagination.html" %}

frappe.pages['track-and-trace'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: '',
		single_column: true
	});

	wrapper.TraceAndTrack = new bloomstack.track_and_trace.TraceAndTrack(wrapper);
}

frappe.pages['track-and-trace'].refresh = function (wrapper) {
	$(window).on('beforeunload', function() {
		wrapper.TraceAndTrack.beforeunload()
	});
}

bloomstack.delay = function(milliseconds) {
	return new Promise((resolve) => {
		setTimeout(function() {
			resolve(milliseconds);
		}, milliseconds);
	});
}

bloomstack.cancelable = function(pr) {
	const _cancelable = {
		was_canceled: false,
		ifNotCanceled(fn) {
			return (data) => {
				if ( !_cancelable.was_canceled ) {
					return fn(data);
				}
			}
		},

		ifCanceled(fn) {
			return (data) => {
				if ( _cancelable.was_canceled ) {
					return fn(data);
				}
			}
		}
	};

	_cancelable.promise = new Promise(function(resolve, reject) {
		_cancelable.cancel = function() {
			_cancelable.was_canceled = true;
			_cancelable.reason = 'canceled';
			reject(_cancelable);
		}

		pr.then((data) => {
				_cancelable.data = data;
				if ( _cancelable.was_canceled ) {
					reject(_cancelable);
				} else {
					resolve(_cancelable);
				}

				return data;
			}, (err) => {
				_cancelable.err = err;
				_cancelable.reason = 'error';
				reject(_cancelable);
			});
	});

	return _cancelable;
};

bloomstack.track_and_trace.TraceAndTrack = class {
	constructor(wrapper) {
		this.wrapper = $(wrapper).find('.layout-main-section');
		this.page = wrapper.page;
		this.search_delay = null;
		this.search_query = null;
		this.current_page = 0;
		this.total_pages = 0;
		this.page_size = 20;

		const assets = [
			'assets/bloomstack_core/css/track_and_trace.css'
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
			},
			() => {
				frappe.dom.unfreeze();
			},
			() => this.page.set_title(__('Track And Trace'))
		]);
	}

	prepare_dom() {
		let me = this;
		let html = frappe.render_template('track_and_trace_main', this);
		this.wrapper.empty().append(html);

		this.wrapper.find('input.search-input:first')
			.focus()
			.on('keyup', function(e) {
			me.search($(this).val());
		});

		this.wrapper.find('.collapse-fields button').click(function() {
			if ( $(this).data('hidden') ) {
				me.wrapper.find('.results .node').removeClass('hide-fields');
				$(this).data('hidden', false);
			} else {
				me.wrapper.find('.results .node').addClass('hide-fields');
				$(this).data('hidden', true);
			}

			me.update_field_toggle_label();

		});

		this.update_field_toggle_label();
	}

	update_field_toggle() {
		// makes sure that field toggle is predictable, even if one node
		// has visible fields, next toggle click will close first.
		this.wrapper.find('.collapse-fields button')
			.data('hidden', this.wrapper.find('.node.hide-fields').length > 0);

		this.update_field_toggle_label();
	}

	update_field_toggle_label() {
		let label = this.wrapper.find('.collapse-fields button').data('hidden') === true?'Show':'Hide';
		this.wrapper.find('.collapse-fields button').text(`${label} Fields`);
	}

	_render_node($container, dt, dn, query_data, cancelable) {
		const me = this;
		let ifNotCanceled = (fn) => (data) => fn(data);
		if ( cancelable !== undefined ) {
			ifNotCanceled = cancelable.ifNotCanceled;
		}

		return bloomstack.track_and_trace.modules
			.query(dt, dn, query_data)
			.then((data) => {
				// keeping microtemplate happy...
				data.is_first = query_data.is_first !== undefined?query_data.is_first: false;
				data.is_last = query_data.is_last !== undefined?query_data.is_last: false;
				data.tree_depth = query_data.tree_depth || 0;
				return data;
			})
			.then(ifNotCanceled((data) => bloomstack.track_and_trace.modules.format(data)))
			.then(ifNotCanceled((data) => {
				return Promise.resolve(bloomstack.track_and_trace.modules.render(dt, dn, data))
					.then((html) => {
						return {
							html,
							data
						}
					});
			}))
			.then(ifNotCanceled((result) => {
				const { html, data } = result;
				if ( html ) {
					let $el = $(html);
					$container.append($el);
					$el.data('query_data', data);
					$el.find('.node-handle').click(function() {
						me.toggle_node($el);
					});

					// default field toggle to current global field toggle setting
					if ( this.wrapper.find('.collapse-fields button').data('hidden') ) {
						$el.addClass('hide-fields')
					} else {
						$el.removeClass('hide-fields')
					}

					$el.find('.leaf:first > .content .actions .field-collapse').click(function(e) {
						$el.toggleClass('hide-fields');
						if ( e.ctrlKey ) {
							if ( $el.hasClass('hide-fields') ) {
								$el.find('.node').addClass('hide-fields');
							} else {
								$el.find('.node').removeClass('hide-fields');
							}
						}

						me.update_field_toggle();
						e.stopPropagation();
						return false;
					});
					bloomstack.track_and_trace.modules.after_render(dt, dn, $el)
					return $el;
				}
			}));
	}

	_run_search(text, current_page) {
		if ( typeof current_page === undefined ) {
			current_page = this.current_page;
		}

		if ( current_page < 0 ) {
			current_page = 0;
		}

		if ( current_page > this.total_pages ) {
			current_page = this.total_pages - 1;
		}

		let _cancelable = bloomstack.cancelable(
			frappe.call({
				method: 'bloomstack_core.bloomstack_core.page.track_and_trace.track_and_trace.search',
				freeze: false,
				args: {
					text,
					start: current_page * this.page_size,
					limit: this.page_size
				}
			})
		);

		_cancelable.promise.then((c) => {
			let data = c.data.message;

			this.wrapper.find('.results').empty();
			if ( data.length > 0 ) {
				this.current_page = current_page;
				this.total_pages = Math.ceil(data[0][2] / this.page_size);
				if ( this.current_page >= this.total_pages ) {
					this.current_page = total_pages - 1;
				}

				this.render_pager({
					current_page: this.current_page,
					total_pages: this.total_pages,
					search: text
				});
			}

			let p = Promise.resolve();
			data.forEach((row) => {
				const dt = row[0];
				const dn = row[1];

				p = p.then(() =>
					this._render_node(this.wrapper.find('.results'), dt, dn, {
						parents: {},
						search_dt: dt,
						search_dn: dn
					}, _cancelable)
				);
			});
		});

		return _cancelable;
	}

	render_pager(paginator_data) {
		let me = this;
		let $paginator = this.wrapper.find('.paginator-top').empty();
		let $paginator_controls = $(frappe.render_template("track_and_trace_pagination", paginator_data));
		$paginator.append($paginator_controls);

		$paginator_controls.find('.first').click(function() {
			me._pagination_go_to_page(paginator_data.search, 0);
		})

		$paginator_controls.find('.prev').click(function() {
			me._pagination_go_to_page(paginator_data.search, paginator_data.current_page - 1);
		})

		$paginator_controls.find('.last').click(function() {
			me._pagination_go_to_page(paginator_data.search, paginator_data.total_pages - 1);
		})

		$paginator_controls.find('.next').click(function() {
			me._pagination_go_to_page(paginator_data.search, paginator_data.current_page + 1);
		})

		$paginator_controls.find('.current-page').change(function(e) {
			let page = parseInt($(this).val() || 1) - 1;
			me._pagination_go_to_page(paginator_data.search, page);
		});
	}

	_pagination_go_to_page(text, page) {
		if ( this.search_query ) {
			this.search_query.cancel();
		}

		this.search_query = this._run_search(text, page);
	}

	toggle_node($el) {
		let data = $el.data('query_data');
		let $container = $el.find('.children:first');
		if ( $el.hasClass('children-loaded') ) {
			if ( $el.hasClass('open') ) {
				$container.slideUp(200);
				$el.removeClass('open');
			} else {
				$container.slideDown(200);
				$el.addClass('open');
			}
		} else {
			$container.slideDown(200);
			$el.addClass('children-loaded')
			$el.addClass('open')
			$el.addClass('loading')

			if ( data.children.length > 0 ) {
				data.children.reduce((p, ch, index, allChildren) => {
						ch.is_first = index === 0;
						ch.is_last = index === allChildren.length - 1;
						ch.tree_depth = (data.tree_depth || 0) + 1;
						return p.then(() => this._render_node($container, ch.dt, ch.dn, ch));
					}, Promise.resolve())
					.then(()=> {
						$el.removeClass('loading');
					});
			}
		}
	}

	search(text) {
		if ( this.search_delay ) {
			this.search_delay.cancel();
			this.search_delay = null;
		}

		if ( text ) {

			this.search_delay = bloomstack.cancelable(bloomstack.delay(500));
			this.search_delay
				.promise.then((c) => {
					this.search_query = this._run_search(text, 0);
				})
				.catch((c) => {
					if ( c.err ) {
						console.error(c.err);
					} else if ( !c.was_canceled ) {
						console.error(c);
					}
					if ( c.was_canceled && this.search_query ) {
						this.search_query.cancel();
					}
				});

		}
	}

	beforeunload() {

	}
}