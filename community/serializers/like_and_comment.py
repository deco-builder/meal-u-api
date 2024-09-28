from rest_framework import serializers
from ..models import RecipeLike, RecipeComment, MealKitLike, MealKitComment, MealKitSave

# Recipe serializers
class RecipeLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeLike
        fields = ['id', 'recipe', 'user', 'liked_at']

class RecipeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeComment
        fields = ['id', 'recipe', 'user', 'comment', 'commented_at']

# MealKit serializers
class MealKitLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealKitLike
        fields = ['id', 'mealkit', 'user', 'liked_at']

class MealKitCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealKitComment
        fields = ['id', 'mealkit', 'user', 'comment', 'commented_at']
