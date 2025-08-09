import frappe
import json
from frappe import _

@frappe.whitelist()
def get_packages():
    """Get all available packages"""
    try:
        packages = frappe.get_all('Package', 
            fields=['name', 'package_name', 'price', 'channels'],
            order_by='package_name'
        )
        return packages
    except Exception as e:
        frappe.log_error(f"Error getting packages: {str(e)}", "Cable Service Management")
        return []

@frappe.whitelist()
def get_package_details(package_names):
    """Get details of selected packages"""
    try:
        if isinstance(package_names, str):
            package_names = json.loads(package_names)
        
        packages = []
        total_price = 0
        
        for name in package_names:
            package = frappe.get_doc('Package', name)
            package_data = {
                'name': package.name,
                'package_name': package.package_name,
                'price': package.price,
                'channels': package.channels
            }
            packages.append(package_data)
            total_price += package.price
        
        return {
            'packages': packages,
            'total_price': total_price
        }
    except Exception as e:
        frappe.log_error(f"Error getting package details: {str(e)}", "Cable Service Management")
        return {'packages': [], 'total_price': 0}

@frappe.whitelist()
def create_customer_profile(customer_data, selected_packages):
    """Create customer profile with selected packages"""
    try:
        if isinstance(customer_data, str):
            customer_data = json.loads(customer_data)
        if isinstance(selected_packages, str):
            selected_packages = json.loads(selected_packages)
        
        # Check if customer with same CNIC already exists
        existing_customer = frappe.db.exists('Customer', {'cnic': customer_data.get('cnic')})
        if existing_customer:
            frappe.throw(_("Customer with this CNIC already exists"))
        
        # Create customer
        customer = frappe.get_doc({
            'doctype': 'Customer',
            'customer_name': customer_data.get('customer_name'),
            'phone': customer_data.get('phone'),
            'address': customer_data.get('address'),
            'cnic': customer_data.get('cnic'),
            'seller': frappe.session.user
        })
        customer.insert()
        
        # Create customer packages
        for package_name in selected_packages:
            customer_package = frappe.get_doc({
                'doctype': 'Customer Package',
                'customer': customer.name,
                'package': package_name
            })
            customer_package.insert()
        
        # Create initial service activation record
        service_activation = frappe.get_doc({
            'doctype': 'Service Activation',
            'customer': customer.name,
            'status': 'Pending'
        })
        service_activation.insert()
        
        frappe.db.commit()
        
        return {
            'success': True,
            'customer_id': customer.name,
            'message': _('Customer profile created successfully')
        }
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error creating customer profile: {str(e)}", "Cable Service Management")
        return {
            'success': False,
            'message': str(e)
        }

@frappe.whitelist()
def record_payment(payment_data):
    """Record customer payment"""
    try:
        if isinstance(payment_data, str):
            payment_data = json.loads(payment_data)
        
        # Create payment record
        payment = frappe.get_doc({
            'doctype': 'Payment',
            'customer': payment_data.get('customer'),
            'amount': payment_data.get('amount'),
            'payment_mode': payment_data.get('payment_mode'),
            'payment_status': payment_data.get('payment_status'),
            'posting_date': frappe.utils.nowdate()
        })
        payment.insert()
        
        frappe.db.commit()
        
        return {
            'success': True,
            'payment_id': payment.name,
            'message': _('Payment recorded successfully')
        }
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error recording payment: {str(e)}", "Cable Service Management")
        return {
            'success': False,
            'message': str(e)
        }

@frappe.whitelist()
def get_customer_status(customer_id):
    """Get customer status and details"""
    try:
        # Get customer details
        customer = frappe.get_doc('Customer', customer_id)
        
        # Get customer packages
        customer_packages = frappe.get_all('Customer Package',
            filters={'customer': customer_id},
            fields=['package', 'activation_date', 'expiry_date']
        )
        
        packages_data = []
        total_amount = 0
        
        for cp in customer_packages:
            package = frappe.get_doc('Package', cp.package)
            packages_data.append({
                'package_name': package.package_name,
                'price': package.price,
                'channels': package.channels,
                'activation_date': cp.activation_date,
                'expiry_date': cp.expiry_date
            })
            total_amount += package.price
        
        # Get service activation status
        service_activation = frappe.get_doc('Service Activation', {'customer': customer_id})
        
        # Get payment status
        payments = frappe.get_all('Payment',
            filters={'customer': customer_id},
            fields=['amount', 'payment_status', 'posting_date'],
            order_by='posting_date desc'
        )
        
        return {
            'customer': {
                'name': customer.customer_name,
                'phone': customer.phone,
                'address': customer.address,
                'cnic': customer.cnic
            },
            'packages': packages_data,
            'total_amount': total_amount,
            'service_status': service_activation.status,
            'activation_date': service_activation.activation_date,
            'payments': payments
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting customer status: {str(e)}", "Cable Service Management")
        return None