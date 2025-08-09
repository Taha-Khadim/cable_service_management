import frappe
from frappe.model.document import Document

class CustomerPackage(Document):
    def validate(self):
        # Validate customer and package exist
        if not frappe.db.exists("Customer", self.customer):
            frappe.throw("Invalid customer selected")
        
        if not frappe.db.exists("Package", self.package):
            frappe.throw("Invalid package selected")
        
        # Check for duplicate customer-package combination
        existing = frappe.db.exists("Customer Package", {
            "customer": self.customer,
            "package": self.package,
            "name": ["!=", self.name]
        })
        if existing:
            frappe.throw("This package is already assigned to the customer")