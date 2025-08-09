import frappe
from frappe.model.document import Document

class Customer(Document):
    def validate(self):
        # Validate CNIC format (basic validation)
        if self.cnic and len(self.cnic) != 13:
            frappe.throw("CNIC must be 13 digits long")
        
        # Validate phone number
        if self.phone and len(self.phone) < 10:
            frappe.throw("Phone number must be at least 10 digits")
    
    def before_save(self):
        # Set default seller if not set
        if not self.seller:
            self.seller = frappe.session.user

    def after_insert(self):
        # Create a pending service activation record for this customer
        activation = frappe.get_doc({
            "doctype": "Service Activation",
            "customer": self.name,
            "status": "Pending",
        })
        activation.insert(ignore_permissions=True)
