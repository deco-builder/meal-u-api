from django.urls import path
from .views.recipes import RecipesView
from .views.recipe_details import RecipeDetailsView

urlpatterns = [
    path("recipes/", RecipesView.as_view(), name="Recipes"),
    path("recipe/<int:recipe_id>/", RecipeDetailsView.as_view(), name="Recipe Details"),
]
