# routing.py
from django.urls import re_path
from community.views.consumers import LikeRecipeConsumer, CommentRecipeConsumer, LikeMealKitConsumer, CommentMealKitConsumer

websocket_urlpatterns = [
    # Routing for Recipe Likes
    re_path(r'ws/recipe/(?P<recipe_id>\d+)/like/$', LikeRecipeConsumer.as_asgi()),

    # Routing for Recipe Comments
    re_path(r'ws/recipe/(?P<recipe_id>\d+)/comment/$', CommentRecipeConsumer.as_asgi()),

    # Routing for MealKit Likes
    re_path(r'ws/mealkit/(?P<mealkit_id>\d+)/like/$', LikeMealKitConsumer.as_asgi()),

    # Routing for MealKit Comments
    re_path(r'ws/mealkit/(?P<mealkit_id>\d+)/comment/$', CommentMealKitConsumer.as_asgi()),
]
