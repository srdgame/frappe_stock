# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class StockItem(Document):
	pass


def stock_item_query(doctype, txt, searchfield, start, page_len, filters):
	if not filters:
		return frappe.db.sql("""select name, item_name from `tabStock Item`
				where %s like %s order by name limit %s, %s""" %
				(searchfield, "%s", "%s", "%s"),
				("%%%s%%" % txt, start, page_len), as_list=1)

	if filters["from"] == "serial_no":
		return frappe.db.sql("""select name, item_name from `tabStock Item`
			where has_serial_no = 1
			and %s like %s order by name limit %s, %s""" %
			(searchfield, "%s", "%s", "%s"),
			("%%%s%%" % txt, start, page_len), as_list=1)
	if filters["from"] == "batch_no":
		return frappe.db.sql("""select name, item_name from `tabStock Item`
			where has_batch_no = 1
			and %s like %s order by name limit %s, %s""" %
			(searchfield, "%s", "%s", "%s"),
			("%%%s%%" % txt, start, page_len), as_list=1)
