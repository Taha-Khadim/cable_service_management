import frappe
from frappe.model.document import Document

class Payment(Document):
    def validate(self):
        # Validate amount is positive
        if self.amount <= 0:
            frappe.throw("Payment amount must be greater than 0")
        
        # Validate customer exists
        if not frappe.db.exists("Customer", self.customer):
            frappe.throw("Invalid customer selected")
    
    def on_update(self):
        # Auto-activate service when payment is marked as Paid
        if self.payment_status == "Paid":
            self.activate_customer_service()
    
    def activate_customer_service(self):
        # Update or create service activation
        existing_activation = frappe.db.exists("Service Activation", {"customer": self.customer})
        
        if existing_activation:
            activation = frappe.get_doc("Service Activation", existing_activation)
            activation.status = "Active"
            activation.activation_date = frappe.utils.nowdate()
            activation.save(ignore_permissions=True)
        else:
            activation = frappe.get_doc({
                "doctype": "Service Activation",
                "customer": self.customer,
                "status": "Active",
                "activation_date": frappe.utils.nowdate()
            })
            activation.insert(ignore_permissions=True)
        
        # Update customer packages to Active
        customer_packages = frappe.get_all("Customer Package", 
            filters={"customer": self.customer},
            fields=["name"]
        )
        
        for pkg in customer_packages:
            cp = frappe.get_doc("Customer Package", pkg.name)
            cp.status = "Active"
            cp.activation_date = frappe.utils.nowdate()
            cp.expiry_date = frappe.utils.add_days(frappe.utils.nowdate(), 30)  # 30 days validity
            cp.save(ignore_permissions=True)