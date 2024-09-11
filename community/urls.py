from django.urls import path
from .views.recipes import RecipesView

urlpatterns = [
    path("recipes/", RecipesView.as_view(), name="Recipes"),
]
