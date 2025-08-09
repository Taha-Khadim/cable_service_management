import frappe
from frappe.model.document import Document

class ServiceActivation(Document):
    def validate(self):
        # Validate customer exists
        if not frappe.db.exists("Customer", self.customer):
            frappe.throw("Invalid customer selected")
        
        # Set activation date when status is changed to Active
        if self.status == "Active" and not self.activation_date:
            self.activation_date = frappe.utils.nowdate()