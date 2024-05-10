// Copyright (c) 2024, Farsi Ansari and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Order CM"] = {
	"filters": [
		{
			'fieldname': 'name',
			'label': 'Sales Order Name',
			'fieldtype': 'Link',
			'options': 'Sales Order'
		},
		{
			'fieldname': 'item_name',
			'label': 'Item Name',
			'fieldtype': 'Link',
			'options': 'Item'
		},
		{
			'fieldname': 'from_date',
			'label': 'From Date',
			'fieldtype': 'Date'
		},
		{
			'fieldname': 'to_date',
			'label': 'To Date',
			'fieldtype': 'Date'
		}
	]
};
