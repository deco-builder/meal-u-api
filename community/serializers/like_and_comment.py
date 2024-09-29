from rest_framework import serializers
from ..models import RecipeLike, RecipeComment, MealKitLike, MealKitComment, MealKitSave

# Recipe serializers
class RecipeLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeLike
        fields = ['id', 'recipe', 'user', 'liked_at']

class RecipeCommentSerializer(serializers.ModelSerializer):
    is_creator = serializers.SerializerMethodField()

    class Meta:
        model = RecipeComment
        fields = ['id', 'recipe', 'user', 'comment', 'commented_at', 'is_creator']
    
    def get_is_creator(self, obj):
        return obj.user == obj.recipe.creator

# MealKit serializers
class MealKitLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealKitLike
        fields = ['id', 'mealkit', 'user', 'liked_at']

class MealKitCommentSerializer(serializers.ModelSerializer):
    is_creator = serializers.SerializerMethodField()

    class Meta:
        model = MealKitComment
        fields = ['id', 'mealkit', 'user', 'comment', 'commented_at', 'is_creator']
    
    def get_is_creator(self, obj):
        return obj.user == obj.mealkit.creator
