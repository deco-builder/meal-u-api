from django.urls import path
from .views.recipes import RecipesView, CommunityRecipesView, TrendingRecipesView, TrendingCreatorView, TopCreatorDietaryView
from .views.recipe_details import RecipeDetailsView, RecipeView
from .views.mealkits import MealKitsView, TrendingMealKitsView, CommunityMealKitsView
from .views.mealkit_details import MealkitDetailsView, MealKitView
from .views.meal_type import MealTypeView
from .views.like_and_comment import RecipeStatsView, RecipeCommentListView, MealKitStatsView, MealKitCommentListView, RecipeLikeView, RecipeCommentView, MealKitLikeView, MealKitCommentView

urlpatterns = [
    path("recipes/", RecipesView.as_view(), name="Recipes"),
    path("recipe/", RecipeView.as_view(), name="Recipe"),
    path("recipe/<int:recipe_id>/", RecipeDetailsView.as_view(), name="Recipe Details"),
    path("mealkits/", MealKitsView.as_view(), name="Mealkits"),
    path("mealkit/", MealKitView.as_view(), name="Mealkit"),
    path("mealkit/<int:mealkit_id>/", MealkitDetailsView.as_view(), name="Mealkit Details"),
    path('recipe/<int:recipe_id>/like/', RecipeLikeView.as_view(), name='recipe-like'),
    path('recipe/<int:recipe_id>/comment/', RecipeCommentView.as_view(), name='recipe-comment'),
    path('mealkit/<int:mealkit_id>/like/', MealKitLikeView.as_view(), name='mealkit-like'),
    path('mealkit/<int:mealkit_id>/comment/', MealKitCommentView.as_view(), name='mealkit-comment'),
    path('recipe/<int:recipe_id>/stats/', RecipeStatsView.as_view(), name='recipe-stats'),
    path('recipe/<int:recipe_id>/comments/', RecipeCommentListView.as_view(), name='recipe-comments'),
    path('mealkit/<int:mealkit_id>/stats/', MealKitStatsView.as_view(), name='mealkit-stats'),
    path('mealkit/<int:mealkit_id>/comments/', MealKitCommentListView.as_view(), name='mealkit-comments'),
    path("meal-types/", MealTypeView.as_view(), name="Meal Types"),
    path("community-recipes/", CommunityRecipesView.as_view(), name="community-recipes"),
    path("trending-recipes/", TrendingRecipesView.as_view(), name="trending-recipes"),
    path("trending-mealkits/", TrendingMealKitsView.as_view(), name="trending-mealkits"),
    path("community-mealkits/", CommunityMealKitsView.as_view(), name="community-mealkits"),
    path("trending-creator/", TrendingCreatorView.as_view(), name="trending-creator"),
    path("top-creator-by-dietary-detail/", TopCreatorDietaryView.as_view(), name="top-creator-by-dietary-detail"),
]
