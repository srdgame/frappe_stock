# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.model.document import Document


class StockEntry(Document):
	def __in_station(self, item_type, item_id, qty):
		doc = frappe.get_doc({
			"doctype": "Stock Item History",
			"inout": 'IN',
			"item_type": item_type,
			"item": item_id,
			"position_type": "Cell Station",
			"position": self.warehouse,
			"qty": qty,
			"uom": frappe.get_value("Stock Item", item_id, "stock_uom"),
			"remark": self.name
		}).insert()

	def __out_station(self, item_type, item_id, qty):
		doc = frappe.get_doc({
			"doctype": "Stock Item History",
			"inout": 'OUT',
			"item_type": item_type,
			"item": item_id,
			"position_type": "Cell Station",
			"position": self.warehouse,
			"qty": qty,
			"uom": frappe.get_value("Stock Item", item_id, "stock_uom"),
			"remark": self.name
		}).insert()

	def validate(self):
		if self.purpose == 'Material Transfer' and not self.source_warehouse:
			throw(_("Source Warehouse is required"))
		for item in self.items:
			item.uom = frappe.get_value("Stock Item", item.item_type, "stock_uom")
			item.item_name = frappe.get_value("Stock Item", item.item_type, "item_name")
			if item.serial_no:
				item.batch_no = frappe.get_value("Stock Serial No", item.serial_no, "batch_no")
				item.qty = 1
				doc = frappe.get_doc("Stock Serial No", item.serial_no)
				if not doc:
					throw(_("Serial NO is not validate! {0}").format(item.serial_no))
				if doc.warehouse and doc.warehouse != self.source_warehouse:
					throw(_("Serial NO {0} is not in Warehouse {1} but in {2}").format(
						item.serial_no, self.source_warehouse, doc.warehouse))
			else:
				item_type = 'Stock Batch No'
				item_id = item.batch_no
				if not item.batch_no:
					item_type = 'Stock Item'
					item_id = item.item_type
				self.__in_station(item_type, item_id, item.qty)

	def on_submit(self):
		for item in self.items:
			if not item.serial_no:
				continue
			doc = frappe.get_doc("Stock Serial No", item.serial_no)
			if not doc:
				throw(_("Serial NO is not validate! {0}").format(item.serial_no))
			if doc.warehouse and doc.warehouse != self.source_warehouse:
				throw(_("Serial NO {0} is not in Warehouse {1} but in {2}").format(
					item.serial_no, self.source_warehouse, doc.warehouse))
			doc.warehouse = self.warehouse
			doc.save()

	def on_cancel(self):
		for item in self.items:
			if item.serial_no:
				doc = frappe.get_doc("Stock Serial No", item.serial_no)
				if not doc:
					throw(_("Serial NO is not validate! {0}").format(item.serial_no))
				if doc.warehouse != self.warehouse:
					throw(_("Serial NO {0} is not in Warehouse {1}").format(
						item.serial_no, doc.warehouse))
				doc.warehouse = self.source_warehouse
				doc.save()
			else:
				item_type = 'Stock Batch No'
				item_id = item.batch_no
				if not item.batch_no:
					item_type = 'Stock Item'
					item_id = item.item_type
				self.__out_station(item_type, item_id, item.qty)