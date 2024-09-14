from django.urls import path
from .views.recipes import RecipesView
from .views.recipe_details import RecipeDetailsView
from .views.mealkits import MealKitsView
from .views.mealkit_details import MealkitDetailsView

urlpatterns = [
    path("recipes/", RecipesView.as_view(), name="Recipes"),
    path("recipe/<int:recipe_id>/", RecipeDetailsView.as_view(), name="Recipe Details"),
    path("mealkits/", MealKitsView.as_view(), name="Mealkits"),
    path("mealkit/<int:mealkit_id>/", MealkitDetailsView.as_view(), name="Mealkit Details"),
]
