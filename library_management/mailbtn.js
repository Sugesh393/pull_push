frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        frm.add_custom_button("Send Mail", () => {
            frm.trigger("mail_dialog");
        })

        frm.add_custom_button("Custom Update", () => {
            frm.trigger("item_dialog");
        })

        frm.add_custom_button("Custom Invoice", () => {
            frm.trigger("custom_sales_invoice");
        })
    },

    mail_dialog: function(frm) {
        let d = new frappe.ui.Dialog({
            title: "Enter Details",
            fields: [
                {
                    fieldname: "email",
                    fieldtype: "Data",
                    label: "Email",
                    reqd: 1
                },
                {
                    fieldname: "body",
                    fieldtype: "Text",
                    label: "Body",
                    reqd: 1
                }
            ],
            size: "medium",
            primary_action_label: "Send",
            primary_action: () => {
                var data = d.get_values();
                //console.log(data.email, data.body, frm.doc.name);
                frappe.call({
                    method: "library_management.mailbtn.sendmail",
                    args: {
                        email: data.email,
                        body: data.body,
                        sub: frm.doc.name
                    },
                    callback: function(r) {
                        frappe.msgprint(r);
                    }
                });
                d.hide();
            }
        });

        d.show();
    },

    item_dialog: function(frm) {
        let data = frm.doc["items"].map((d) => {
           return {
               docname: d.name,
               name: d.name,
               item_code: d.item_code,
               delivery_date: d.delivery_date,
               qty: d.qty,
               rate: d.rate
           } 
        });

        let fields = [
            {
                fieldtype: "Data",
                fieldname: "docname",
                read_only: 1,
                hidden: 1,
            },
            {
                fieldname: "item_code",
                fieldtype: "Link",
                label: "Item Code",
                options: "Item",
                in_list_view: 1
            },
            {
                fieldname: "delivery_date",
                fieldtype: "Date",
                label: "Delivery Date",
                in_list_view: 1
            },
            {
                fieldname: "qty",
                fieldtype: "Float",
                label: "Qty",
                in_list_view: 1
            },
            {
                fieldname: "rate",
                fieldtype: "Currency",
                label: "Rate",
                options: "currency",
                in_list_view: 1
            }
        ]

        let i = new frappe.ui.Dialog({
            title: "Update Items",
            size: "extra-large",
            fields: [
                {
                    fieldname: "trans_items",
                    fieldtype: "Table",
                    label: "Items",
                    reqd: 1,
                    data: data,
                    get_data: () => {
                        return data;
                    },
                    fields: fields
                }
            ],
            
            primary_action_label: "Update",
            primary_action: () => {
                const trans_items = i.get_values()["trans_items"].filter((item) => !!item.item_code);
                console.log(trans_items);
                frappe.call({
                    method: "library_management.mailbtn.update_items",
                    args: {
                        parent_doctype: frm.doc.doctype,
                        trans_items: trans_items,
                        parent_doctype_name: frm.doc.name
                    },
                    callback: function() {
                        frm.reload_doc();
                    }
                })
                i.hide();
                refresh_field("items");
            }
        })
        i.show();
    },

    custom_sales_invoice: function(frm) {
        // frappe.model.open_mapped_doc({
        //     method: "library_management.mailbtn.custom_sales_invoice",
        //     frm: frm
        // });

        // frappe.call({
        //     method: "library_management.mailbtn.custom_sales_invoice",
        //     args: {
        //         source: frm.doc
        //     },
        //     callback: function(r) {
        //         frappe.model.sync(r.message);
        //         frappe.set_route("Form", r.message.doctype, r.message.name);
        //     }
        // });

        frappe.call({
            method: "library_management.stock_entry.auto_stock_issue",
            // callback: function(r) {
            //     // frappe.set_route("Form", "Stock Entry");
            //     frappe.msgprint(r.message);
            // }
        })
    }
})