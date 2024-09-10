from django.contrib import admin
from django.apps import apps
from .models import Item
from user_auth.models import User, Employee, EmployeeRoles, DeliveryCouriers

admin.site.register(Item)
admin.site.register(User)
admin.site.register(EmployeeRoles)
admin.site.register(Employee)
admin.site.register(DeliveryCouriers)

# Register models from specific apps dynamically
def get_models_from_app(app_name):
    app = apps.get_app_config(app_name)
    models = app.get_models()

    for model in models:
        admin.site.register(model)

get_models_from_app('community')
get_models_from_app('groceries')
get_models_from_app('orders')
get_models_from_app('users')