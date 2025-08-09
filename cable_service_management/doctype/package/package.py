import frappe
from frappe.model.document import Document

class Package(Document):
    def validate(self):
        # Validate price is positive
        if self.price <= 0:
            frappe.throw("Package price must be greater than 0")
        
        # Ensure package name is unique
        existing = frappe.db.exists("Package", {"package_name": self.package_name, "name": ["!=", self.name]})
        if existing:
            frappe.throw(f"Package with name '{self.package_name}' already exists")