import frappe, json
from frappe.utils import flt
from frappe.model.mapper import get_mapped_doc

from erpnext.stock.get_item_details import (
	_get_item_tax_template,
	get_item_tax_map,
	get_conversion_factor
)
from frappe.utils.data import getdate

@frappe.whitelist()
def sendmail(email, body, sub):
	frappe.sendmail(
		recipients=email,
		message=body,
		subject=sub
	)
	return "Mail Sent to User"

def add_taxes_from_tax_template(child_item, parent_doc, db_insert=True):
	add_taxes_from_item_tax_template = frappe.db.get_single_value(
		"Accounts Settings", "add_taxes_from_item_tax_template"
	)

	print("Out of if")
	if child_item.get("item_tax_rate") and add_taxes_from_item_tax_template:
		print("In of if")
		tax_map = json.loads(child_item.get("item_tax_rate"))
		for tax_type in tax_map:
			tax_rate = flt(tax_map[tax_type])
			taxes = parent_doc.get("taxes") or []
			# add new row for tax head only if missing
			found = any(tax.account_head == tax_type for tax in taxes)
			if not found:
				tax_row = parent_doc.append("taxes", {})
				tax_row.update(
					{
						"description": str(tax_type).split(" - ")[0],
						"charge_type": "On Net Total",
						"account_head": tax_type,
						"rate": tax_rate,
					}
				)

				if db_insert:
					tax_row.db_insert()
								   
		print("1", tax_map.as_dict())
	  
def set_child_tax_template_and_map(item, child_item, parent_doc):
	args = {
		"item_code": item.item_code,
		"posting_date": parent_doc.transaction_date,
		"tax_category": parent_doc.get("tax_category"),
		"company": parent_doc.get("company"),
	}

	child_item.item_tax_template = _get_item_tax_template(args, item.taxes)
	if child_item.get("item_tax_template"):
		child_item.item_tax_rate = get_item_tax_map(
			parent_doc.get("company"), child_item.item_tax_template, as_json=True
		)
	
	print("2", child_item.as_dict())
			
def validate_and_delete_children(parent, data) -> bool:
	deleted_children = []
	updated_item_names = [d.get("docname") for d in data]
	for item in parent.items:
		if item.name not in updated_item_names:
			deleted_children.append(item)

	for d in deleted_children:
		d.cancel()
		d.delete()

	parent.update_prevdoc_status()

	return bool(deleted_children)

@frappe.whitelist()
def update_items(parent_doctype, trans_items, parent_doctype_name, child_docname="items"):
	
	data= json.loads(trans_items)
	removed = False

	parent = frappe.get_doc(parent_doctype, parent_doctype_name)
	child_doctype = "Sales Order Item"
	
	removed_items = validate_and_delete_children(parent, data)
	removed |= removed_items
	
	for d in data:
		if not d.get("docname"):
			removed = True
			child_item = frappe.new_doc(child_doctype, parent_doc=parent, parentfield=child_docname)
			item = frappe.get_doc("Item", d.get("item_code"))

			for field in ("item_code", "item_name", "description", "item_group"):
				child_item.update({field: item.get(field)})

			date_fieldname = "delivery_date"
			child_item.update({date_fieldname: d.get(date_fieldname)})
			child_item.stock_uom = item.stock_uom
			child_item.uom = item.stock_uom
			conversion_factor = flt(get_conversion_factor(item.item_code, child_item.uom).get("conversion_factor"))
			child_item.conversion_factor = conversion_factor

			# print("3", child_item.as_dict())

			set_child_tax_template_and_map(item, child_item, parent)
			add_taxes_from_tax_template(child_item, parent)
		
		else:
			child_item = frappe.get_doc(child_doctype, d.get("docname"))

			prev_code, new_code = flt(child_item.get("item_code")), flt(d.get("item_code"))
			prev_qty, new_qty = flt(child_item.get("qty")), flt(d.get("qty"))
			prev_rate, new_rate = flt(child_item.get("rate")), flt(d.get("rate"))
			prev_date, new_date = child_item.get("delivery_date"), d.get("delivery_date")

			if (prev_qty == new_qty) and (prev_rate == new_rate) and (prev_date == new_date) and (prev_code == new_code):
				continue  

		if (child_item.get("item_code") != flt(d.get("item_code"))):
			child_item.qty = flt(d.get("qty"))

		if (child_item.get("rate") != flt(d.get("rate"))):
			child_item.rate = flt(d.get("rate"))

		if (child_item.get("delivery_date") != d.get("delivery_date")):
			child_item.delivery_date = d.get("delivery_date")

		child_item.amount = flt(d.get("qty")) * flt(d.get("rate"))

		child_item.save()

	parent.reload()  
	parent.save()
	
	if removed:
		parent.update_prevdoc_status()

@frappe.whitelist()
def custom_sales_invoice(source):
	# def update_date(source, target_doc, source_parent):
	# 	target_doc.due_date = getdate()

	# def update_income(source, target_doc, source_parent):
	# 	for i in source_parent.items:
	# 		item = frappe.get_doc("Item", i.item_code).as_dict()

	# 		if item.item_defaults[0]["company"] == source_parent.company:
	# 			target_doc.income_account = item.item_defaults[0]["income_account"]
		
	# doclist = get_mapped_doc(
	# 	"Sales Order",
	# 	source,
	# 	{
	# 		"Sales Order": {
	# 			"doctype": "Sales Invoice",
	# 			"postprocess": update_date,
	# 		},
	# 		"Sales Order Item": {
	# 			"doctype": "Sales Invoice Item",
	# 			"postprocess": update_income,
	# 		},
	# 		"Sales Taxes and Charges": {
	# 			"doctype": "Sales Taxes and Charges",
	# 			"add_if_empty": True,
	# 		},
	# 		"Sales Team": {
	# 			"doctype": "Sales Team",
	# 			"add_if_empty": True,
	# 		},
	# 	},
	# 	target_doc,
	# 	ignore_permissions=True,
	# )
	source = json.loads(source)
	
	inv = frappe.new_doc("Sales Invoice")
	
	inv.posting_date = getdate()
	inv.customer = source.get("customer")
	inv.company = source.get("company")
	inv.due_date = inv.posting_date
	
	for i in source["items"]:
		item = frappe.get_doc("Item", i["item_code"]).as_dict()
		i["cost_center"] = source["taxes"][0]["cost_center"]
		i["income_account"] = item.item_defaults[0]["income_account"]

		inv.append("items", i)

	inv.update({"taxes": source["taxes"]})

	return inv
