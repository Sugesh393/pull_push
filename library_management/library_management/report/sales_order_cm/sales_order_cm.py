# Copyright (c) 2024, Farsi Ansari and contributors
# For license information, please see license.txt

import frappe


def execute(filters={}):
	columns, data = [], []

	columns = get_columns()
	# sales_data = get_sales_data(filters)

	# data = sales_data
	# if not sales_data:
	# 	frappe.msgprint("No records found")
	# 	return columns, sales_data
	
	# for d in sales_data:
	# 	row = frappe._dict({
	# 		'name': d.name,
	# 		'item_code': d.item_code,
	# 		'qty': d.qty,
	# 		'delivery_date': d.delivery_date,
	# 		'rate': d.rate,
	# 		'amount': d.amount
	# 	})
	# 	data.append(row)
 
	call = "1 = 1"
	if filters.name:
		call += f" and t1.name = '{filters.name}'"
	if filters.item_name:
		call += f" and t2.item_code = '{filters.item_name}'"
	if filters.from_date:
		call += f" and t2.delivery_date >= '{filters.from_date}'"
	if filters.to_date:
		call += f" and t2.delivery_date <= '{filters.to_date}'"

	query = f""" 
				SELECT t1.name, t2.item_code, t2.qty, t2.delivery_date, t2.rate, t2.amount
				FROM `tabSales Order` as t1
				INNER JOIN `tabSales Order Item` as t2 ON t2.parent = t1.name
				WHERE {call}
				ORDER BY t1.name ASC
			""" # Join used for joining child table
	
	data = frappe.db.sql(query, as_dict=1)

	return columns, data

def get_columns():
	return [
		{
			'fieldname': 'name',
			'label': 'Sales Order Name',
			'fieldtype': 'Data',
			'width': '200'
		},
		{
			'fieldname': 'item_code',
			'label': 'Item Code',
			'fieldtype': 'Data',
			'width': '200'
		},
		{
			'fieldname': 'qty',
			'label': 'Quantity',
			'fieldtype': 'Float',
			'width': '100'
		},
		{
			'fieldname': 'delivery_date',
			'label': 'Delivery Date',
			'fieldtype': 'Date',
			'width': '120'
		},
		{
			'fieldname': 'rate',
			'label': 'Rate',
			'fieldtype': 'Float',
			'width': '100'
		},
		{
			'fieldname': 'amount',
			'label': 'Amount',
			'fieldtype': 'Float',
			'width': '100'
		}
	]

# def get_sales_data(filters):
# 	res = get_condition(filters)
# 	print(res)

# 	data = frappe.get_all(
# 		doctype='Sales Order',
# 		fields=['name', 'items.item_code', 'items.qty', 'items.delivery_date', 'items.rate', 'items.amount'],
# 		filters=res
# 	)
	
# 	return data

# def get_condition(filters):
# 	res = {}
# 	f = 0
# 	t = 0
# 	for key, value in filters.items():
# 		if filters.get(key):
# 			if key == "from_date": # mistake - mentioned filters.get(key) instead key
# 				res['delivery_date'] = ['>=', filters.from_date]
# 				f = 1
# 			elif key == "to_date":
# 				res['delivery_date'] = ['<=', filters.to_date]
# 				t = 1
# 			else:
# 				res[key] = value

# 	if (f == 1) and (t == 1): # mistake - f == t
# 		res['delivery_date'] = ['between', [filters.from_date, filters.to_date]]
# 	return res