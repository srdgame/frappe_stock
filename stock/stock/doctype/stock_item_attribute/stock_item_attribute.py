# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class StockItemAttribute(Document):
	pass


attribute_type_map = {
	"batch": "batch_attribute",
	"serial": "serial_attribute"
}

'''
def stock_item_attribute_query(doctype, txt, searchfield, start, page_len, filters):
	if not filters:
		return frappe.db.sql("""select name, attribute from `tabStock Item Attribute`
			where %s like %s order by name limit %s, %s""" %
			(searchfield, "%s", "%s", "%s"),
			("%%%s%%" % txt, start, page_len), as_list=1)

	typ = attribute_type_map[filters["type"]] or ""
	item_code = filters["item_code"] or ""
	return frappe.db.sql("""select name, attribute from `tabStock Item Attribute`
		where parentfield = %s and parent = %s
		and %s like %s order by name limit %s, %s""" %
		("%s", "%s", searchfield, "%s", "%s", "%s"),
		(typ, item_code, "%%%s%%" % txt, start, page_len), as_list=1)
'''