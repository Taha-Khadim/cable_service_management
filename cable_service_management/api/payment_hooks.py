import frappe

def auto_activate_service(doc, method=None):
    # Only activate if status is Paid
    if doc.payment_status == "Paid":
        existing = frappe.get_all("Service Activation", filters={"customer": doc.customer})
        if existing:
            activation = frappe.get_doc("Service Activation", existing[0].name)
            activation.status = "Active"
            activation.activation_date = frappe.utils.nowdate()
            activation.save(ignore_permissions=True)
        else:
            activation = frappe.get_doc({
                "doctype": "Service Activation",
                "customer": doc.customer,
                "status": "Active",
                "activation_date": frappe.utils.nowdate()
            })
            activation.insert(ignore_permissions=True)
