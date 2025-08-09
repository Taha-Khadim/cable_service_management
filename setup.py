import frappe
import os
import json

def create_doctypes():
    # Create Package DocType
    if not frappe.db.exists("DocType", "Package"):
        doc = frappe.new_doc("DocType")
        doc.update({
            "module": "Cable Service Management",
            "custom": 1,
            "fields": [
                {"label": "Package Name", "fieldname": "package_name", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"label": "Price", "fieldname": "price", "fieldtype": "Currency", "reqd": 1},
                {"label": "Channels", "fieldname": "channels", "fieldtype": "Text", "reqd": 1},
                {"label": "Description", "fieldname": "description", "fieldtype": "Text Editor"}
            ],
            "permissions": [
                {"role": "System Manager", "permlevel": 0, "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Seller", "permlevel": 0, "read": 1, "write": 1, "create": 1, "delete": 0}
            ],
            "autoname": "hash",
            "search_fields": "package_name"
        })
        doc.insert()
    
    # Create Customer DocType
    if not frappe.db.exists("DocType", "Customer"):
        doc = frappe.new_doc("DocType")
        doc.update({
            "module": "Cable Service Management",
            "custom": 1,
            "fields": [
                {"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data", "reqd": 1},
                {"label": "Phone", "fieldname": "phone", "fieldtype": "Data", "reqd": 1},
                {"label": "Address", "fieldname": "address", "fieldtype": "Text", "reqd": 1},
                {"label": "CNIC", "fieldname": "cnic", "fieldtype": "Data", "reqd": 1, "unique": 1},
                {"label": "Email", "fieldname": "email", "fieldtype": "Data", "options": "Email"},
                {"label": "Status", "fieldname": "status", "fieldtype": "Select", "options": "\nPending\nActive\nInactive", "default": "Pending", "read_only": 1}
            ],
            "permissions": [
                {"role": "System Manager", "permlevel": 0, "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Seller", "permlevel": 0, "read": 1, "write": 1, "create": 1, "delete": 0}
            ],
            "autoname": "hash",
            "search_fields": "customer_name, phone, cnic"
        })
        doc.insert()
    
    # Create Customer Package DocType
    if not frappe.db.exists("DocType", "Customer Package"):
        doc = frappe.new_doc("DocType")
        doc.update({
            "module": "Cable Service Management",
            "custom": 1,
            "fields": [
                {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "reqd": 1},
                {"label": "Package", "fieldname": "package", "fieldtype": "Link", "options": "Package", "reqd": 1},
                {"label": "Status", "fieldname": "status", "fieldtype": "Select", "options": "\nPending\nActive\nInactive", "default": "Pending", "reqd": 1},
                {"label": "Activation Date", "fieldname": "activation_date", "fieldtype": "Date", "read_only": 1},
                {"label": "Expiry Date", "fieldname": "expiry_date", "fieldtype": "Date", "read_only": 1}
            ],
            "permissions": [
                {"role": "System Manager", "permlevel": 0, "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Seller", "permlevel": 0, "read": 1, "write": 1, "create": 1, "delete": 0}
            ],
            "autoname": "hash",
            "search_fields": "customer, package"
        })
        doc.insert()
    
    # Create Payment DocType
    if not frappe.db.exists("DocType", "Payment"):
        doc = frappe.new_doc("DocType")
        doc.update({
            "module": "Cable Service Management",
            "custom": 1,
            "fields": [
                {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "reqd": 1},
                {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "reqd": 1},
                {"label": "Payment Mode", "fieldname": "payment_mode", "fieldtype": "Select", "options": "\nCash\nBank Transfer\nCredit Card\nMobile Wallet", "reqd": 1},
                {"label": "Payment Status", "fieldname": "payment_status", "fieldtype": "Select", "options": "\nPaid\nPending", "default": "Pending", "reqd": 1},
                {"label": "Date", "fieldname": "date", "fieldtype": "Date", "default": "Today", "reqd": 1},
                {"label": "Transaction ID", "fieldname": "transaction_id", "fieldtype": "Data"},
                {"label": "Notes", "fieldname": "notes", "fieldtype": "Small Text"}
            ],
            "permissions": [
                {"role": "System Manager", "permlevel": 0, "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Seller", "permlevel": 0, "read": 1, "write": 1, "create": 1, "delete": 0}
            ],
            "autoname": "hash",
            "search_fields": "customer, date, payment_status"
        })
        doc.insert()

def create_pages():
    # Ensure the www directory exists
    www_path = frappe.get_app_path("cable_service_management", "www")
    if not os.path.exists(www_path):
        os.makedirs(www_path)
    
    # Create Package Details Page
    if not frappe.db.exists("Page", "package-details"):
        doc = frappe.new_doc("Page")
        doc.update({
            "module": "Cable Service Management",
            "title": "Package Details",
            "published": 1,
            "script": """
                frappe.ready(function() {
                    load_packages();
                    
                    $(document).on('click', '.select-package', function() {
                        var package_name = $(this).data('package');
                        var selected_packages = JSON.parse(localStorage.getItem('selected_packages') || '[]');
                        
                        if ($(this).hasClass('selected')) {
                            $(this).removeClass('selected btn-success').addClass('btn-primary');
                            $(this).text('Select');
                            selected_packages = selected_packages.filter(p => p !== package_name);
                        } else {
                            $(this).removeClass('btn-primary').addClass('selected btn-success');
                            $(this).text('Selected');
                            selected_packages.push(package_name);
                        }
                        
                        localStorage.setItem('selected_packages', JSON.stringify(selected_packages));
                        update_total_price();
                    });
                    
                    $('#proceed-to-profile').click(function() {
                        var selected_packages = JSON.parse(localStorage.getItem('selected_packages') || '[]');
                        if (selected_packages.length === 0) {
                            frappe.msgprint('Please select at least one package');
                            return;
                        }
                        frappe.set_route('user-profile');
                    });
                });
                
                function load_packages() {
                    frappe.call({
                        method: "cable_service_management.api.get_packages",
                        callback: function(r) {
                            if (r.message) {
                                render_packages(r.message);
                            }
                        }
                    });
                }
                
                function render_packages(packages) {
                    var container = $('#packages-container');
                    container.empty();
                    
                    packages.forEach(function(package) {
                        var package_html = `
                            <div class="package-card col-md-4 mb-4">
                                <div class="card">
                                    <div class="card-body">
                                        <h5 class="card-title">${package.package_name}</h5>
                                        <p class="card-text"><strong>Price:</strong> ${package.price}</p>
                                        <p class="card-text"><strong>Channels:</strong> ${package.channels}</p>
                                        ${package.description ? `<p class="card-text">${package.description}</p>` : ''}
                                        <button class="btn btn-primary select-package" data-package="${package.name}">Select</button>
                                    </div>
                                </div>
                            </div>
                        `;
                        container.append(package_html);
                    });
                }
                
                function update_total_price() {
                    var selected_packages = JSON.parse(localStorage.getItem('selected_packages') || '[]');
                    if (selected_packages.length === 0) {
                        $('#total-price').text('0');
                        return;
                    }
                    
                    frappe.call({
                        method: "cable_service_management.api.get_packages_total",
                        args: { package_names: selected_packages },
                        callback: function(r) {
                            if (r.message) {
                                $('#total-price').text(r.message);
                            }
                        }
                    });
                }
            """,
            "standard": "Yes"
        })
        doc.insert()
        
        # Create HTML for the page
        html_content = """
        <div class="container">
            <h1>Available Packages</h1>
            <div class="row mb-4">
                <div class="col-md-12">
                    <div class="alert alert-info">
                        <strong>Total Price: <span id="total-price">0</span></strong>
                    </div>
                </div>
            </div>
            <div class="row" id="packages-container">
                <!-- Packages will be loaded here -->
            </div>
            <div class="row mt-4">
                <div class="col-md-12 text-center">
                    <button class="btn btn-primary btn-lg" id="proceed-to-profile">Proceed to Customer Profile</button>
                </div>
            </div>
        </div>
        """
        
        # Save the HTML content to a file
        with open(os.path.join(www_path, "package-details.html"), "w") as f:
            f.write(html_content)
    
    # Create User Profile Page
    if not frappe.db.exists("Page", "user-profile"):
        doc = frappe.new_doc("Page")
        doc.update({
            "module": "Cable Service Management",
            "title": "User Profile",
            "published": 1,
            "script": """
                frappe.ready(function() {
                    var selected_packages = JSON.parse(localStorage.getItem('selected_packages') || '[]');
                    if (selected_packages.length === 0) {
                        frappe.set_route('package-details');
                        return;
                    }
                    
                    frappe.call({
                        method: "cable_service_management.api.get_packages_by_names",
                        args: { package_names: selected_packages },
                        callback: function(r) {
                            if (r.message) {
                                render_selected_packages(r.message);
                            }
                        }
                    });
                    
                    $('#create-profile').click(function() {
                        if (!$('#customer-form')[0].checkValidity()) {
                            $('#customer-form')[0].reportValidity();
                            return;
                        }
                        
                        var customer_data = {
                            customer_name: $('#customer_name').val(),
                            phone: $('#phone').val(),
                            address: $('#address').val(),
                            cnic: $('#cnic').val(),
                            email: $('#email').val()
                        };
                        
                        frappe.call({
                            method: "cable_service_management.api.create_customer",
                            args: { customer_data: customer_data },
                            callback: function(r) {
                                if (r.message) {
                                    var customer_name = r.message;
                                    localStorage.setItem('customer_name', customer_name);
                                    
                                    var promises = selected_packages.map(function(package_name) {
                                        return new Promise(function(resolve, reject) {
                                            frappe.call({
                                                method: "cable_service_management.api.create_customer_package",
                                                args: { 
                                                    customer_name: customer_name,
                                                    package_name: package_name
                                                },
                                                callback: function(r) {
                                                    if (r.message) {
                                                        resolve(r.message);
                                                    } else {
                                                        reject();
                                                    }
                                                }
                                            });
                                        });
                                    });
                                    
                                    Promise.all(promises).then(function() {
                                        frappe.set_route('payment');
                                    }).catch(function() {
                                        frappe.msgprint('There was an error creating customer packages');
                                    });
                                } else {
                                    frappe.msgprint('There was an error creating the customer profile');
                                }
                            }
                        });
                    });
                    
                    $('#back-to-packages').click(function() {
                        frappe.set_route('package-details');
                    });
                });
                
                function render_selected_packages(packages) {
                    var container = $('#selected-packages');
                    container.empty();
                    
                    var total_price = 0;
                    packages.forEach(function(package) {
                        total_price += package.price;
                        var package_html = `
                            <div class="selected-package mb-2">
                                <strong>${package.package_name}</strong> - ${package.price}
                            </div>
                        `;
                        container.append(package_html);
                    });
                    
                    $('#total-price').text(total_price);
                }
            """,
            "standard": "Yes"
        })
        doc.insert()
        
        # Create HTML for the page
        html_content = """
        <div class="container">
            <h1>Create Customer Profile</h1>
            <div class="row">
                <div class="col-md-6">
                    <form id="customer-form">
                        <div class="form-group">
                            <label for="customer_name">Customer Name *</label>
                            <input type="text" class="form-control" id="customer_name" required>
                        </div>
                        <div class="form-group">
                            <label for="phone">Phone *</label>
                            <input type="text" class="form-control" id="phone" required>
                        </div>
                        <div class="form-group">
                            <label for="address">Address *</label>
                            <textarea class="form-control" id="address" rows="3" required></textarea>
                        </div>
                        <div class="form-group">
                            <label for="cnic">CNIC *</label>
                            <input type="text" class="form-control" id="cnic" required>
                        </div>
                        <div class="form-group">
                            <label for="email">Email</label>
                            <input type="email" class="form-control" id="email">
                        </div>
                        <div class="form-group">
                            <button type="button" class="btn btn-secondary" id="back-to-packages">Back</button>
                            <button type="button" class="btn btn-primary" id="create-profile">Create Profile</button>
                        </div>
                    </form>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            Selected Packages
                        </div>
                        <div class="card-body">
                            <div id="selected-packages">
                                <!-- Selected packages will be loaded here -->
                            </div>
                            <hr>
                            <div class="total-price">
                                <strong>Total Price: <span id="total-price">0</span></strong>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        
        # Save the HTML content to a file
        with open(os.path.join(www_path, "user-profile.html"), "w") as f:
            f.write(html_content)
    
    # Create Payment Page
    if not frappe.db.exists("Page", "payment"):
        doc = frappe.new_doc("Page")
        doc.update({
            "module": "Cable Service Management",
            "title": "Payment",
            "published": 1,
            "script": """
                frappe.ready(function() {
                    var customer_name = localStorage.getItem('customer_name');
                    if (!customer_name) {
                        frappe.set_route('package-details');
                        return;
                    }
                    
                    frappe.call({
                        method: "cable_service_management.api.get_customer_packages",
                        args: { customer_name: customer_name },
                        callback: function(r) {
                            if (r.message) {
                                render_packages(r.message);
                            }
                        }
                    });
                    
                    $('#record-payment').click(function() {
                        if (!$('#payment-form')[0].checkValidity()) {
                            $('#payment-form')[0].reportValidity();
                            return;
                        }
                        
                        var payment_data = {
                            customer: customer_name,
                            amount: $('#total-amount').val(),
                            payment_mode: $('#payment_mode').val(),
                            payment_status: $('#payment_status').val(),
                            transaction_id: $('#transaction_id').val(),
                            notes: $('#notes').val()
                        };
                        
                        frappe.call({
                            method: "cable_service_management.api.create_payment",
                            args: { payment_data: payment_data },
                            callback: function(r) {
                                if (r.message) {
                                    if ($('#payment_status').val() === 'Paid') {
                                        frappe.call({
                                            method: "cable_service_management.api.update_customer_status",
                                            args: { 
                                                customer_name: customer_name,
                                                status: 'Active'
                                            },
                                            callback: function(r) {
                                                if (r.message) {
                                                    frappe.msgprint('Payment recorded successfully. Customer status updated to Active.');
                                                    frappe.set_route('status');
                                                }
                                            }
                                        });
                                    } else {
                                        frappe.msgprint('Payment recorded successfully.');
                                        frappe.set_route('status');
                                    }
                                } else {
                                    frappe.msgprint('There was an error recording the payment');
                                }
                            }
                        });
                    });
                    
                    $('#back-to-profile').click(function() {
                        frappe.set_route('user-profile');
                    });
                });
                
                function render_packages(packages) {
                    var container = $('#packages-list');
                    container.empty();
                    
                    var total_amount = 0;
                    packages.forEach(function(pkg) {
                        total_amount += pkg.price;
                        var package_html = `
                            <tr>
                                <td>${pkg.package_name}</td>
                                <td>${pkg.price}</td>
                            </tr>
                        `;
                        container.append(package_html);
                    });
                    
                    $('#total-amount').val(total_amount);
                }
            """,
            "standard": "Yes"
        })
        doc.insert()
        
        # Create HTML for the page
        html_content = """
        <div class="container">
            <h1>Payment</h1>
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            Selected Packages
                        </div>
                        <div class="card-body">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>Package</th>
                                        <th>Price</th>
                                    </tr>
                                </thead>
                                <tbody id="packages-list">
                                    <!-- Packages will be loaded here -->
                                </tbody>
                                <tfoot>
                                    <tr>
                                        <th>Total</th>
                                        <th id="total-amount-display">0</th>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <form id="payment-form">
                        <div class="form-group">
                            <label for="total-amount">Total Amount</label>
                            <input type="text" class="form-control" id="total-amount" readonly>
                        </div>
                        <div class="form-group">
                            <label for="payment_mode">Payment Mode *</label>
                            <select class="form-control" id="payment_mode" required>
                                <option value="">Select Payment Mode</option>
                                <option value="Cash">Cash</option>
                                <option value="Bank Transfer">Bank Transfer</option>
                                <option value="Credit Card">Credit Card</option>
                                <option value="Mobile Wallet">Mobile Wallet</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="payment_status">Payment Status *</label>
                            <select class="form-control" id="payment_status" required>
                                <option value="">Select Payment Status</option>
                                <option value="Paid">Paid</option>
                                <option value="Pending">Pending</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="transaction_id">Transaction ID</label>
                            <input type="text" class="form-control" id="transaction_id">
                        </div>
                        <div class="form-group">
                            <label for="notes">Notes</label>
                            <textarea class="form-control" id="notes" rows="3"></textarea>
                        </div>
                        <div class="form-group">
                            <button type="button" class="btn btn-secondary" id="back-to-profile">Back</button>
                            <button type="button" class="btn btn-primary" id="record-payment">Record Payment</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        """
        
        # Save the HTML content to a file
        with open(os.path.join(www_path, "payment.html"), "w") as f:
            f.write(html_content)
    
    # Create Status Page
    if not frappe.db.exists("Page", "status"):
        doc = frappe.new_doc("Page")
        doc.update({
            "module": "Cable Service Management",
            "title": "Status",
            "published": 1,
            "script": """
                frappe.ready(function() {
                    var customer_name = localStorage.getItem('customer_name');
                    if (!customer_name) {
                        frappe.set_route('package-details');
                        return;
                    }
                    
                    frappe.call({
                        method: "cable_service_management.api.get_customer_details",
                        args: { customer_name: customer_name },
                        callback: function(r) {
                            if (r.message) {
                                render_customer_details(r.message);
                            }
                        }
                    });
                    
                    $('#new-customer').click(function() {
                        localStorage.removeItem('selected_packages');
                        localStorage.removeItem('customer_name');
                        frappe.set_route('package-details');
                    });
                    
                    $('#view-all-customers').click(function() {
                        window.location.href = '/app/customer';
                    });
                });
                
                function render_customer_details(customer) {
                    $('#customer-name').text(customer.customer_name);
                    $('#customer-phone').text(customer.phone);
                    $('#customer-address').text(customer.address);
                    $('#customer-cnic').text(customer.cnic);
                    $('#customer-email').text(customer.email || 'N/A');
                    
                    var status_class = '';
                    if (customer.status === 'Active') {
                        status_class = 'badge-success';
                    } else if (customer.status === 'Pending') {
                        status_class = 'badge-warning';
                    } else {
                        status_class = 'badge-danger';
                    }
                    
                    $('#customer-status').html(`<span class="badge ${status_class}">${customer.status}</span>`);
                    
                    var packages_html = '';
                    customer.packages.forEach(function(pkg) {
                        var pkg_status_class = '';
                        if (pkg.status === 'Active') {
                            pkg_status_class = 'badge-success';
                        } else if (pkg.status === 'Pending') {
                            pkg_status_class = 'badge-warning';
                        } else {
                            pkg_status_class = 'badge-danger';
                        }
                        
                        packages_html += `
                            <tr>
                                <td>${pkg.package_name}</td>
                                <td>${pkg.price}</td>
                                <td><span class="badge ${pkg_status_class}">${pkg.status}</span></td>
                            </tr>
                        `;
                    });
                    
                    $('#packages-list').html(packages_html);
                }
            """,
            "standard": "Yes"
        })
        doc.insert()
        
        # Create HTML for the page
        html_content = """
        <div class="container">
            <h1>Customer Status</h1>
            <div class="card mb-4">
                <div class="card-header">
                    Customer Information
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>Name:</strong> <span id="customer-name"></span></p>
                            <p><strong>Phone:</strong> <span id="customer-phone"></span></p>
                            <p><strong>Email:</strong> <span id="customer-email"></span></p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Address:</strong> <span id="customer-address"></span></p>
                            <p><strong>CNIC:</strong> <span id="customer-cnic"></span></p>
                            <p><strong>Status:</strong> <span id="customer-status"></span></p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card mb-4">
                <div class="card-header">
                    Package Details
                </div>
                <div class="card-body">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Package</th>
                                <th>Price</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody id="packages-list">
                            <!-- Packages will be loaded here -->
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="mt-4">
                <button class="btn btn-primary" id="new-customer">Create New Customer</button>
                <button class="btn btn-secondary" id="view-all-customers">View All Customers</button>
            </div>
        </div>
        """
        
        # Save the HTML content to a file
        with open(os.path.join(www_path, "status.html"), "w") as f:
            f.write(html_content)

def create_api_methods():
    api_file_content = """
import frappe
import json

@frappe.whitelist()
def get_packages():
    try:
        return frappe.get_all('Package', fields=['name', 'package_name', 'price', 'channels', 'description'])
    except Exception as e:
        frappe.log_error(f"Error getting packages: {str(e)}", "Cable Service Management")
        return []

@frappe.whitelist()
def get_packages_by_names(package_names):
    try:
        if isinstance(package_names, str):
            package_names = json.loads(package_names)
        
        packages = []
        for name in package_names:
            package = frappe.get_doc('Package', name)
            packages.append({
                'name': package.name,
                'package_name': package.package_name,
                'price': package.price,
                'channels': package.channels,
                'description': package.description
            })
        
        return packages
    except Exception as e:
        frappe.log_error(f"Error getting packages by names: {str(e)}", "Cable Service Management")
        return []

@frappe.whitelist()
def get_packages_total(package_names):
    try:
        if isinstance(package_names, str):
            package_names = json.loads(package_names)
        
        total = 0
        for name in package_names:
            package = frappe.get_doc('Package', name)
            total += package.price
        
        return total
    except Exception as e:
        frappe.log_error(f"Error calculating packages total: {str(e)}", "Cable Service Management")
        return 0

@frappe.whitelist()
def create_customer(customer_data):
    try:
        if isinstance(customer_data, str):
            customer_data = json.loads(customer_data)
        
        if frappe.db.exists('Customer', {'cnic': customer_data.get('cnic')}):
            existing_customer = frappe.get_doc('Customer', {'cnic': customer_data.get('cnic')})
            return existing_customer.name
        
        customer = frappe.new_doc('Customer')
        customer.update(customer_data)
        customer.insert()
        return customer.name
    except Exception as e:
        frappe.log_error(f"Error creating customer: {str(e)}", "Cable Service Management")
        return None

@frappe.whitelist()
def create_customer_package(customer_name, package_name):
    try:
        if frappe.db.exists('Customer Package', {
            'customer': customer_name,
            'package': package_name
        }):
            return frappe.get_doc('Customer Package', {
                'customer': customer_name,
                'package': package_name
            }).name
        
        customer_package = frappe.new_doc('Customer Package')
        customer_package.update({
            'customer': customer_name,
            'package': package_name,
            'status': 'Pending'
        })
        customer_package.insert()
        return customer_package.name
    except Exception as e:
        frappe.log_error(f"Error creating customer package: {str(e)}", "Cable Service Management")
        return None

@frappe.whitelist()
def get_customer_packages(customer_name):
    try:
        packages = frappe.get_all('Customer Package', 
            filters={'customer': customer_name},
            fields=['package', 'status']
        )
        
        package_details = []
        for pkg in packages:
            package_doc = frappe.get_doc('Package', pkg.package)
            package_details.append({
                'package_name': package_doc.package_name,
                'price': package_doc.price,
                'status': pkg.status
            })
        
        return package_details
    except Exception as e:
        frappe.log_error(f"Error getting customer packages: {str(e)}", "Cable Service Management")
        return []

@frappe.whitelist()
def create_payment(payment_data):
    try:
        if isinstance(payment_data, str):
            payment_data = json.loads(payment_data)
        
        payment = frappe.new_doc('Payment')
        payment.update(payment_data)
        payment.insert()
        return payment.name
    except Exception as e:
        frappe.log_error(f"Error creating payment: {str(e)}", "Cable Service Management")
        return None

@frappe.whitelist()
def update_customer_status(customer_name, status):
    try:
        customer = frappe.get_doc('Customer', customer_name)
        customer.status = status
        customer.save()
        
        customer_packages = frappe.get_all('Customer Package', 
            filters={'customer': customer_name}
        )
        
        for pkg in customer_packages:
            doc = frappe.get_doc('Customer Package', pkg.name)
            doc.status = status
            
            if status == 'Active' and not doc.activation_date:
                doc.activation_date = frappe.utils.nowdate()
                doc.expiry_date = frappe.utils.add_days(frappe.utils.nowdate(), 30)
            
            doc.save()
        
        return True
    except Exception as e:
        frappe.log_error(f"Error updating customer status: {str(e)}", "Cable Service Management")
        return False

@frappe.whitelist()
def get_customer_details(customer_name):
    try:
        customer = frappe.get_doc('Customer', customer_name)
        
        customer_packages = frappe.get_all('Customer Package', 
            filters={'customer': customer_name}
        )
        
        packages = []
        overall_status = 'Inactive'
        
        for pkg in customer_packages:
            doc = frappe.get_doc('Customer Package', pkg.name)
            package_doc = frappe.get_doc('Package', doc.package)
            
            packages.append({
                'package_name': package_doc.package_name,
                'price': package_doc.price,
                'status': doc.status,
                'activation_date': doc.activation_date,
                'expiry_date': doc.expiry_date
            })
            
            if doc.status == 'Active':
                overall_status = 'Active'
            elif doc.status == 'Pending' and overall_status != 'Active':
                overall_status = 'Pending'
        
        return {
            'customer_name': customer.customer_name,
            'phone': customer.phone,
            'address': customer.address,
            'cnic': customer.cnic,
            'email': customer.email,
            'status': overall_status,
            'packages': packages
        }
    except Exception as e:
        frappe.log_error(f"Error getting customer details: {str(e)}", "Cable Service Management")
        return None
"""
    
    with open(frappe.get_app_path("cable_service_management", "api.py"), "w") as f:
        f.write(api_file_content)

def create_role():
    if not frappe.db.exists("Role", "Seller"):
        doc = frappe.new_doc("Role")
        doc.update({
            "role_name": "Seller",
            "desk_access": 1,
            "restrict_to_domain": ""
        })
        doc.insert()

def create_sample_data():
    if frappe.db.count("Package") == 0:
        packages = [
            {"package_name": "News", "price": 500, "channels": "CNN, BBC, Al Jazeera, Fox News, CNBC", "description": "Stay updated with the latest news from around the world."},
            {"package_name": "Sports", "price": 700, "channels": "ESPN, Sky Sports, beIN Sports, Ten Sports", "description": "Never miss a game with our comprehensive sports coverage."},
            {"package_name": "Kids", "price": 400, "channels": "Cartoon Network, Nickelodeon, Disney Channel, Pogo", "description": "Entertainment for children of all ages."},
            {"package_name": "All-in-One", "price": 1500, "channels": "All channels from News, Sports, and Kids packages", "description": "The complete entertainment package for the whole family."}
        ]
        
        for package in packages:
            doc = frappe.new_doc("Package")
            doc.update(package)
            doc.insert()

def setup_application():
    create_doctypes()
    create_pages()
    create_api_methods()
    create_role()
    create_sample_data()
    
    frappe.db.commit()
    print("Cable Service Management application setup completed successfully!")

if __name__ == "__main__":
    setup_application()
