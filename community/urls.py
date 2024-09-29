from django.urls import path
from .views.recipes import RecipesView
from .views.recipe_details import RecipeDetailsView, RecipeView
from .views.mealkits import MealKitsView
from .views.mealkit_details import MealkitDetailsView, MealKitView
from .views.meal_type import MealTypeView

urlpatterns = [
    path("recipes/", RecipesView.as_view(), name="Recipes"),
    path("recipe/", RecipeView.as_view(), name="Recipe"),
    path("recipe/<int:recipe_id>/", RecipeDetailsView.as_view(), name="Recipe Details"),
    path("mealkits/", MealKitsView.as_view(), name="Mealkits"),
    path("mealkit/", MealKitView.as_view(), name="Mealkit"),
    path("mealkit/<int:mealkit_id>/", MealkitDetailsView.as_view(), name="Mealkit Details"),
    path("meal-types/", MealTypeView.as_view(), name="Meal Types"),
]
