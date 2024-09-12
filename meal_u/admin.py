from django.contrib import admin
from django.apps import apps
from .models import Item

admin.site.register(Item)

def get_models_from_app(app_name):
    app = apps.get_app_config(app_name)
    models = app.get_models()

    for model in models:
        admin.site.register(model)

get_models_from_app('user_auth')
get_models_from_app('community')
get_models_from_app('groceries')
get_models_from_app('orders')
get_models_from_app('users')