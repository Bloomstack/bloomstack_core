/* global frappe, bloomstack */
frappe.provide("bloomstack.track_and_trace");

bloomstack.get_doc = (cdt, cdn) => {
    return Promise.resolve(frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: cdt,
            name: cdn
        }
    })).then(r => {
        return r.message;
    });
}

bloomstack.get_value = (doctype, fieldname, filters, parent) => {
    return Promise.resolve(frappe.call({
        method: "frappe.client.get_value",
        args: {
            doctype,
            fieldname,
            filters,
            parent
        }
    })).then(r => {
        return r.message;
    });
}

bloomstack.track_and_trace.default_module = {
    has_route: true,

    route(dt, dn) {
        frappe.set_route("Form", dt, dn);
    },

    after_render(dt, dn, $el) {
        let me = this;
        if ( this.has_route ) {
            let $link = $('<li class="doctype-link btn btn-default fa fa-arrow-right" title="Go to Doctype"></li>')
            $el.find('.title').append($link);
            $link.click(function(e) {
                e.preventDefault();
                me.route(dt, dn);
                return false;
            });
        }

        $el.find('[data-route-dt]').click(function(e) {
            let routeDT = $(this).attr('data-route-dt');
            let routeDN = $(this).attr('data-route-dn');
            if ( routeDT && routeDN ) {
                e.preventDefault();
                me.route(routeDT, routeDN);
                return false;
            }
        })
    }
}

bloomstack.track_and_trace.ModulesManager = class {
    constructor() {
        this.modules = {};
    }

    add(dt, customization) {
        if ( !this.modules.hasOwnProperty(dt) ) {
            this.modules[dt] = [];
        }

        customization = Object.assign({}, bloomstack.track_and_trace.default_module, customization);

        this.modules[dt].push(customization);
    }

    render(dt, dn, data) {
        let render_data = Object.assign({
            format(value, fieldtype) {
                if ( !fieldtype ) {
                    return value;
                }

                return frappe.format(value, { fieldtype }, { only_value: true });
            }
        }, data);

        if ( this.modules.hasOwnProperty(dt) ) {
            const parentHash = `${dt}/${dn}`;
            if ( (data.parents || {}).hasOwnProperty(parentHash) ) {
                return Promise.resolve("");
            }

            return this.modules[dt].reduce((p, c) => {
                if ( c.hasOwnProperty("render" ) ) {
                    return p.then((html) => c.render(dt, dn, render_data, html));
                } else if ( c.hasOwnProperty("template") ) {
                    return p.then((html) => frappe.render_template(c.template, render_data));
                }

                return p.then(html => frappe.render_template("track_and_trace_module_generic", render_data));
            }, Promise.resolve())
        }

        return Promise.resolve(frappe.render_template("track_and_trace_module_generic", render_data));
    }

    after_render(dt, dn, $el) {
        if ( this.modules.hasOwnProperty(dt) ) {
            return this.modules[dt].reduce((p, c) => {
                if ( c.hasOwnProperty("after_render" ) ) {
                    return p.then(($el) => c.after_render(dt, dn, $el));
                }

                return p;
            }, Promise.resolve($el))
        }

        return Promise.resolve();
    }

    query(dt, dn, data) {
        if ( typeof data === undefined ) {
            data = {};
        }

        let result = null;

        if ( this.modules.hasOwnProperty(dt) ) {
            result = this.modules[dt].reduce((p, c) => {
                if ( c.hasOwnProperty("query" ) ) {
                    if ( data.query !== false ) {
                        return p.then((data) => Promise.resolve(c.query(dt, dn, data)));
                    }
                } else {
                    if ( data.query !== false ) {
                        return p.then((data) => this.default_query(dt, dn, data, c));
                    }
                }

                return p;
            }, Promise.resolve(data || {}));
        } else if ( data.query !== false ) {

            result = this.default_query(dt, dn, data);
        } else {
            result = Promise.resolve(data);
        }

        return result.then((r) => {
            r.search_dt = data.search_dt;
            r.search_dn = data.search_dn;
            r.parents = Object.assign({}, data.parents || {});
            this.dedupe_parents(r);
            return r;
        });
    }

    dedupe_parents(node) {
        if ( node.children && node.children.length > 0 ) {
            const parentHash = `${node.dt}/${node.dn}`;
            node.children = node.children.reduce((new_list, child) => {
                let chHash = `${child.dt}/${child.dn}`;
                if ( !node.parents.hasOwnProperty(chHash) ) {
                    child.parents = Object.assign({}, node.parents || {}, {
                        [parentHash]: true
                    });
                    new_list.push(child);
                }

                return new_list
            }, []);
        }
    }

    format(data) {
        const dt = data.dt;
        const dn = data.dn;

        if ( dt && dn && this.modules.hasOwnProperty(dt) ) {
            return this.modules[dt].reduce((p, c) => {
                    if ( c.hasOwnProperty("format" ) ) {
                        return p.then((data) => Promise.resolve(c.format(data)));
                    }

                    return p;
                }, Promise.resolve(data))
                .then((r) => {
                    this.dedupe_parents(r);
                    return r;
                });
        }
        
        return Promise.resolve(data)
            .then((r) => {
                this.dedupe_parents(r);
                return r;
            })
    }

    default_query(dt, dn, query_data, c) {
        return bloomstack.get_doc(dt, dn)
            .then((data) => {
                let children = [];
                if ( data.items ) {
                    
                    children = data.items.map((item) => {
                        let childFields = [];
                        let childIcon = c?c.icon || "fa fa-question": "fa fa-question";
                        if ( this.modules.hasOwnProperty(item.doctype) ) {
                            childFields = this.modules[item.doctype].reduce((p, c) => {
                                if ( c.hasOwnProperty("icon") ) {
                                    childIcon = c.icon;
                                }

                                if ( c.hasOwnProperty("fields") ) {
                                    for(let field of c.fields) {
                                        let existingIdx = p.findIndex((f) => f.field === field.field);
                                        if ( existingIdx > -1 ) {
                                            p.splice(existingIdx, 1, field);
                                        } else {
                                            p.push(field);
                                        }
                                    }
                                }
                                return p;
                            }, []);
                        }
                        return {
                            search_dt: query_data.search_dt,
                            search_dn: query_data.search_dn,
                            query: false,
                            dt: item.doctype,
                            dn: item.name,
                            image_path: null,
                            icon: childIcon,
                            title: `${item.doctype}: ${item.name}`,
                            fields: childFields,
                            data: item,
                            children: []
                        }
                    });
                }
                return {
                    search_dt: query_data.search_dt,
                    search_dn: query_data.search_dn,
                    dt,
                    dn,
                    image_path: null,
                    icon: c?c.icon || "fa fa-question": "fa fa-question",
                    title: `${data.doctype}: ${data.name}`,
                    fields: (c?c.fields || []: []).slice(),
                    data,
                    children
                }
            });
    }
}