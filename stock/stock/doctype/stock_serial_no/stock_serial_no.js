// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stock Serial No', {
	setup: function(frm) {
		frm.fields_dict['attributes'].grid.get_field("attribute").get_query  = function(){
			return {
				filters: {
					"parentfield": "serial_attribute",
					"parent": frm.doc.item_code
				}
			};
		};
		frm.fields_dict['batch_no'].get_query  = function(){
			return {
				filters: {
					"item_code": frm.doc.item_code,
					"docstatus": 1
				}
			};
		};
		frm.fields_dict['item_code'].get_query  = function(){
			return {
				filters: {
					"has_serial_no": 1
				}
			};
		};
	},
	refresh: function(frm) {

	}
});

frappe.ui.form.on("Stock Serial No", "item_code", function(frm) {
	frappe.call({
		type: "GET",
		method:'frappe.desk.search.search_link',
		args: {
			"doctype": "Stock Item Attribute",
			"txt": "",
			"filters": {
				"parentfield": "serial_attribute",
				"parent": frm.doc.item_code
			}
		},
		callback: function (r) {
			frm.set_value("attributes" ,"");
			if (r.results) {
				$.each(r.results, function(i, d) {
					var row = frappe.model.add_child(cur_frm.doc, "Stock Item AttributeValue", "attributes");
					row.attribute = d.value;
					row.attr_name = d.description;
					if(row.attr_name == 'pin_code' || row.attr_name == 'PIN_CODE'
						|| row.attr_name == 'pincode' || row.attr_name == 'PINCODE') {
						var max = 999;
						var min = 0;
						var val = '00' + Math.floor(Math.random()*(max-min+1)+min);
						row.value = val.slice(-3);
					}
				});
			}
			refresh_field("attributes");
		}
	});
});
