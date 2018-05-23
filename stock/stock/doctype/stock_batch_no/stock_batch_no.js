// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stock Batch No', {
	setup: function(frm) {
		frm.fields_dict['attributes'].grid.get_field("attribute").get_query  = function(){
			return {
				filters: {
					"parentfield": "batch_attribute",
					"parent": frm.doc.item_code
				}
			};
		};
		frm.fields_dict['item_code'].get_query  = function(){
			return {
				filters: {
					"has_batch_no": 1
				}
			};
		};
	},
	refresh: function(frm) {

	}
});


frappe.ui.form.on("Stock Batch No", "item_code", function(frm) {
	frappe.call({
		type: "GET",
		method:'frappe.desk.search.search_link',
		args: {
			"doctype": "Stock Item Attribute",
			"txt": "",
			"filters": {
				"parentfield": "batch_attribute",
				"parent": frm.doc.item_code
			}
		},
		callback: function (r) {
			frm.set_value("attributes", "");
			if (r.results) {
				$.each(r.results, function (i, d) {
					var row = frappe.model.add_child(cur_frm.doc, "Stock Item AttributeValue", "attributes");
					row.attribute = d.value;
					row.attr_name = d.description;
				});
			}
			refresh_field("attributes");
		}
	});
});
