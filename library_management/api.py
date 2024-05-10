import frappe

@frappe.whitelist()
def set_sales_order(
    customer,
    order_type,
    date,
    charge_type,
    account_head,
    currency,
    price_list,
    items
):
    #Creating new instance for DocType
    sales = frappe.new_doc("DP Sales Order")
    sales.customer = customer
    sales.order_type = order_type
    sales.date = date
    sales.charge_type = charge_type
    sales.account_head = account_head
    sales.currency = currency
    sales.price_list = price_list

    #For Child Table
    sales.append("item", {
        "item_name": items.get("item_name"),
        "quantity": items.get("quantity"),
        "rate": items.get("rate")
    })

    #Save the record
    sales.insert()
    return "Values stored successfully"

@frappe.whitelist()
def insert_child(value):
    inst = frappe.new_doc("Child Table Task")
    for i in value:
        inst.append("insertion", {
            "name1": i.get("name"),
            "date": i.get("date")
        })
        
    inst.save()
    return "Value Inserted"