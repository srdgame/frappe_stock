// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stock Delivery Order', {
	setup: function(frm) {
		frm.fields_dict['items'].grid.get_field("serial_no").get_query = function (doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				filters: {
					"item_code": d.item,
					"warehouse": frm.doc.warehouse,
					"docstatus": 1
				}
			};
		};
		frm.fields_dict['items'].grid.get_field("batch_no").get_query = function (doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				filters: {
					"item_code": d.item,
					"docstatus": 1
				}
			};
		};
	},
	refresh: function(frm) {

	},
	order_source_type: function(frm) {
		frm.set_value("order_source_id", null);
	}
});

frappe.ui.form.on("Stock Delivery Order", "warehouse", function(frm) {
	frappe.call({
		method: "frappe.client.get_value",
		args: {
			doctype: "Stock Warehouse",
			fieldname: "company",
			filters: { name: frm.doc.warehouse },
		},
		callback: function(r, rt) {
			if(r.message) {
				frm.set_value("company", r.message.company);
			}
		}
	});
});

frappe.ui.form.on('Stock Delivery OrderItem', {
	item: function(doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		frappe.call({
			type: "GET",
			method: "frappe.client.get",
			args: {
				doctype: "Stock Item",
				name: d.item,
				filters: {
					docstatus: 1
				}
			},
			callback: function(r, rt) {
				if(r.message) {
					frappe.model.set_value(cdt, cdn, "item_name", r.message.item_name);
					frappe.model.set_value(cdt, cdn, "uom", r.message.stock_uom);
				}
			}
		});
	},
	serial_no: function(doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.serial_no) {
			frappe.model.set_value(cdt, cdn, "qty", 1);
			if (!d.batch_no) {
				frappe.call({
					type: "GET",
					method: "frappe.client.get_value",
					args: {
						doctype: "Stock Serial No",
						fieldname: "batch_no",
						filters: { name: d.serial_no },
					},
					callback: function (r, rt) {
						frappe.model.set_value(cdt, cdn, "batch_no", r.message.batch_no);
					}
				});
			}
		}
	}
});
