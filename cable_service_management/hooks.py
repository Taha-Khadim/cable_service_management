app_name = "cable_service_management"
app_title = "Cable Service Management"
app_publisher = "Lumora Code"
app_description = "A simple cable/network service management app"
app_email = "lumoracode@gmail.com"
app_license = "MIT"

doc_events = {
    "Payment": {
        "on_update": "cable_service_management.api.payment_hooks.auto_activate_service"
    }
}
