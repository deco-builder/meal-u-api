from rest_framework import serializers
from ..models import RecipeLike, RecipeComment, MealKitLike, MealKitComment, MealKitSave
from .recipes import RecipesSerializer
from .mealkits import MealKitsSerializer
from user_auth.models import User

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'profile_picture']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_profile_picture(self, obj):
        return obj.image.url if obj.image else None

class RecipeLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeLike
        fields = ['id', 'recipe', 'user', 'liked_at']

class RecipeCommentSerializer(serializers.ModelSerializer):
    is_creator = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = RecipeComment
        fields = ['id', 'recipe', 'user', 'comment', 'commented_at', 'is_creator']
    
    def get_is_creator(self, obj):
        return obj.user == obj.recipe.creator

class MealKitLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealKitLike
        fields = ['id', 'mealkit', 'user', 'liked_at']

class MealKitCommentSerializer(serializers.ModelSerializer):
    is_creator = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = MealKitComment
        fields = ['id', 'mealkit', 'user', 'comment', 'commented_at', 'is_creator']
    
    def get_is_creator(self, obj):
        return obj.user == obj.mealkit.creator

class UserRecipeLikeSerializer(serializers.ModelSerializer):
    recipe = RecipesSerializer(read_only=True)

    class Meta:
        model = RecipeLike
        fields = ['recipe', 'liked_at']

class UserMealKitLikeSerializer(serializers.ModelSerializer):
    mealkit = MealKitsSerializer(read_only=True)

    class Meta:
        model = MealKitLike
        fields = ['mealkit', 'liked_at']