from django.urls import path
from .views.categories import CategoryView
from .views.ingredients import IngredientsView
from .views.ingredient_details import IngredientDetailsView

urlpatterns = [
    path("categories/", CategoryView.as_view(), name="Categories"),
    path("ingredients/", IngredientsView.as_view(), name="Ingredients"),
    path(
        "ingredient/<int:ingredient_id>/",
        IngredientDetailsView.as_view(),
        name="Ingredient Details",
    ),
]
