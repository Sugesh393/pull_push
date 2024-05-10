# Copyright (c) 2024, Farsi Ansari and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DPSalesOrder(Document):
	def on_submit(self):
		sales_order = frappe.new_doc("Sales Order")

		sales_order.customer = self.customer
		sales_order.order_type = self.order_type
		sales_order.transaction_date = self.date

		sales_order.currency = self.currency
		sales_order.selling_price_list = self.price_list

		sales_order.append("items", {
			"item_code": self.item[0].item_name,
			"delivery_date": self.date,
			"qty": self.item[0].quantity,
			"rate": self.item[0].rate,
			"description": "Description for Books"
		})

		sales_order.append("taxes", {
			"charge_type": self.charge_type,
			"account_head": self.account_head,
			"description": "TDS",
			"rate": 1
		})

		sales_order.insert()
		pass
