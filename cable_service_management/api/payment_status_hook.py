import frappe

def payment_status_hook(doc, method=None):
    if doc.payment_status == "Paid":
        sa = frappe.get_doc({
            "doctype": "Service Activation",
            "customer": doc.customer,
            "status": "Active"
        })
        sa.insert(ignore_permissions=True)
