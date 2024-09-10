from django.urls import path
from groceries.views.categories import CategoryView

urlpatterns = [
    path("category/", CategoryView.as_view(), name="Category"),
]