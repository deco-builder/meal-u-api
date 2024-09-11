from django.urls import path
from .views.categories import CategoryView
from .views.ingredients import IngredientsView

urlpatterns = [
    path("categories/", CategoryView.as_view(), name="Categories"),
    path("ingredients/", IngredientsView.as_view(), name="Categories"),
]