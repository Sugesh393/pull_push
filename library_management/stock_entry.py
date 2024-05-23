import frappe
import datetime
from datetime import datetime, date, timedelta
from frappe.utils.data import getdate

@frappe.whitelist()
def auto_stock_entry():
    sty = frappe.new_doc("Stock Entry")
    sty.stock_entry_type = "Material Issue"

    b = frappe.get_all(
        "Bin", 
        filters = {
            "actual_qty": ("!=", 0)
        },
        fields = ["item_code", "warehouse", "actual_qty", "ordered_qty", "valuation_rate"],
    )

    for i in b:
        sty.append("items", {
            "item_code": i.get("item_code"),
            "s_warehouse": i.get("warehouse"),
            "qty": i.get("actual_qty"),
            "basic_rate": i.get("valuation_rate"),
            "basic_amount": i.get("valuation_rate")
        })

    sty.save()

@frappe.whitelist()
def auto_stock_issue():
    def stock_creation(sea_doc):
        lt = []
        for i in sea_doc.warehouse:
            lt.append(i.warehouse)

        sty = frappe.new_doc("Stock Entry")
        sty.stock_entry_type = "Material Issue"

        b = frappe.get_all(
            "Bin", 
            filters = {
                "actual_qty": ("!=", 0),
                "warehouse": ("in", lt),
            },
            fields = ["item_code", "warehouse", "actual_qty", "ordered_qty", "valuation_rate"],
        )

        for i in b:
            sty.append("items", {
                "item_code": i.get("item_code"),
                "s_warehouse": i.get("warehouse"),
                "qty": i.get("actual_qty"),
                "basic_rate": i.get("valuation_rate"),
                "basic_amount": i.get("valuation_rate")
            })
        sty.save()
    
    date1 = getdate()
    sea_doc = frappe.get_doc("Scheduled Stock Entry")

    if(sea_doc.get('frequency') == "Weekly"):
        if not sea_doc.get('next_schedule'):
            sea_doc.next_schedule = str(date1)

        ns = date.fromisoformat(sea_doc.get('next_schedule'))
        ed = date.fromisoformat(sea_doc.get('end_date'))
        if(ns < ed):
            if(sea_doc.get('day') == date1.strftime("%A")):
                stock_creation(sea_doc)

                ns = ns + timedelta(days=7)
                sea_doc.next_schedule = ns
                sea_doc.save()
    
    elif(sea_doc.get('frequency') == "Monthly"):
        if not sea_doc.get('next_schedule'):
            sea_doc.next_schedule = sea_doc.get('repeat_on_date')

        ns = date.fromisoformat(sea_doc.get('next_schedule'))
        if(ns.day == int(date1.strftime("%d"))):
            ed = date.fromisoformat(sea_doc.get('end_date'))
            if(ns < ed):
                stock_creation(sea_doc)

                new_month = ns.month
                if new_month > 12:
                    new_year = ns.year + 1
                    new_month -= 12

                ns = date(new_year, new_month, ns.day)
                sea_doc.next_schedule = ns
                sea_doc.save()

    elif(sea_doc.get('frequency') == "Quarter Yearly"):
        if not sea_doc.get('next_schedule'):
            sea_doc.next_schedule = sea_doc.get('repeat_on_date')

        ns = datetime.strptime(sea_doc.get('next_schedule'), "%Y-%m-%d")
        if(ns.day == int(date1.strftime("%d"))):
            ed = datetime.strptime(sea_doc.get('end_date'), "%Y-%m-%d")
            if(ns.year <= ed.year):
                stock_creation(sea_doc)

                new_month = ns.month + 3
                new_year = ns.year
                if new_month > 12:
                    new_year += 1
                    new_month -= 12

                ns = datetime(new_year, new_month, ns.day)
                sea_doc.next_schedule = ns
                sea_doc.save()

    elif(sea_doc.get('frequency') == "Half Yearly"):
        if not sea_doc.get('next_schedule'):
            sea_doc.next_schedule = sea_doc.get('repeat_on_date')

        ns = datetime.strptime(sea_doc.get('next_schedule'), "%Y-%m-%d")
        if(ns.day == int(date1.strftime("%d"))):
            ed = datetime.strptime(sea_doc.get('end_date'), "%Y-%m-%d")
            if(ns.year <= ed.year):
                stock_creation(sea_doc)

                new_month = ns.month + 6
                new_year = ns.year
                if new_month > 12:
                    new_year += 1
                    new_month -= 12

                ns = datetime(new_year, new_month, ns.day)
                sea_doc.next_schedule = ns
                sea_doc.save()

    elif(sea_doc.get('frequency') == "Yearly"):
        if not sea_doc.get('next_schedule'):
            sea_doc.next_schedule = sea_doc.get('repeat_on_date')

        ns = datetime.strptime(sea_doc.get('next_schedule'), "%Y-%m-%d")
        if(ns.day == int(date1.strftime("%d"))):
            ed = datetime.strptime(sea_doc.get('end_date'), "%Y-%m-%d")
            if(ns.year <= ed.year and ns.month == int(date1.strftime("%m"))):
                stock_creation(sea_doc)

                new_year = ns.year + 1
                ns = datetime(new_year, ns.month, ns.day)
                sea_doc.next_schedule = ns
                sea_doc.save()