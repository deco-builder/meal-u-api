from django.urls import path
from .views.recipes import RecipesView
from .views.recipe_details import RecipeDetailsView
from .views.mealkits import MealKitsView

urlpatterns = [
    path("recipes/", RecipesView.as_view(), name="Recipes"),
    path("recipe/<int:recipe_id>/", RecipeDetailsView.as_view(), name="Recipe Details"),
    path("mealkits/", MealKitsView.as_view(), name="Mealkits"),
]
