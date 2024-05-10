# Copyright (c) 2024, Farsi Ansari and contributors
# For license information, please see license.txt

import frappe


def execute(filters={}):
	columns, data = [], []

	columns = get_columns()
	
	query = """ SELECT DISTINCT t1.name as so_name, t2.name as sv_name, t3.name as pe_name, t4.name as dn_name, t2.customer, ct2.item_code, ct2.qty, ct2.rate, t4.posting_date 
			FROM `tabSales Order` as t1 JOIN `tabSales Order Item` as ct1 ON ct1.parent = t1.name 
			JOIN `tabSales Invoice Item` as ct2 ON t1.name = ct2.sales_order JOIN `tabSales Invoice` as t2 ON ct2.parent = t2.name 
			JOIN `tabPayment Entry Reference` as ct3 ON t2.name = ct3.reference_name JOIN `tabPayment Entry` as t3 ON ct3.parent = t3.name
			JOIN `tabDelivery Note Item` as ct4 ON t2.name = ct4.against_sales_invoice JOIN `tabDelivery Note` as t4 ON ct4.parent = t4.name 
			ORDER BY so_name ASC; """
	
	data = frappe.db.sql(query, as_dict=1)
	
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "so_name",
			"label": "Sales OrderName",
			"fieldtype": "Data",
			"width": "190"
		},
		{
			"fieldname": "sv_name",
			"label": "Sales Invoice Name",
			"fieldtype": "Data",
			"width": "190"
		},
		{
			"fieldname": "pe_name",
			"label": "Payment Entry Name",
			"fieldtype": "Data",
			"width": "190"
		},
		{
			"fieldname": "dn_name",
			"label": "Delivery Note Name",
			"fieldtype": "Data",
			"width": "190"
		},
		{
			"fieldname": "customer",
			"label": "Customer",
			"fieldtype": "Data",
			"width": "90"
		},
		{
			"fieldname": "item_code",
			"label": "Item Code",
			"fieldtype": "Data",
			"width": "150"
		},
		{
			"fieldname": "qty",
			"label": "Quantity",
			"fieldtype": "Float",
			"width": "60"
		},
		{
			"fieldname": "rate",
			"label": "Rate",
			"fieldtype": "Float",
			"width": "60"
		},
		{
			"fieldname": "posting_date",
			"label": "Transaction Date",
			"fieldtype": "Date",
			"width": "90"
		}
	]