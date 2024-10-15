from rest_framework import serializers
from ..models import RecipeLike, RecipeComment, MealKitLike, MealKitComment, MealKitSave
from .recipes import RecipesSerializer
from .mealkits import MealKitsSerializer
from user_auth.models import User


class RecipeLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeLike
        fields = ['id', 'recipe', 'user', 'liked_at']

class RecipeCommentSerializer(serializers.ModelSerializer):
    is_creator = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)  
    user_details = serializers.SerializerMethodField(read_only=True)  

    class Meta:
        model = RecipeComment
        fields = ['id', 'recipe', 'user', 'user_details', 'comment', 'commented_at', 'is_creator']

    def get_is_creator(self, obj):
        return obj.user == obj.recipe.creator

    def get_user_details(self, obj):
        # Return user details for read operations
        return {
            "id": obj.user.id,
            "name": f"{obj.user.first_name} {obj.user.last_name}",
            "profile_picture": obj.user.image.url if obj.user.image else None
        }

class MealKitLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealKitLike
        fields = ['id', 'mealkit', 'user', 'liked_at']

class MealKitCommentSerializer(serializers.ModelSerializer):
    is_creator = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)  # Handle write operations
    user_details = serializers.SerializerMethodField(read_only=True)  # Custom field for read operations

    class Meta:
        model = MealKitComment
        fields = ['id', 'mealkit', 'user', 'user_details', 'comment', 'commented_at', 'is_creator']

    def get_is_creator(self, obj):
        return obj.user == obj.mealkit.creator

    def get_user_details(self, obj):
        # Return user details for read operations
        return {
            "id": obj.user.id,
            "name": f"{obj.user.first_name} {obj.user.last_name}",
            "profile_picture": obj.user.image.url if obj.user.image else None
        }

class UserRecipeLikeSerializer(serializers.ModelSerializer):
    recipe = RecipesSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = RecipeLike
        fields = ['recipe', 'liked_at', 'likes_count', 'comments_count']

    def get_likes_count(self, obj):
        return RecipeLike.objects.filter(recipe_id=obj.recipe_id).count()

    def get_comments_count(self, obj):
        return RecipeComment.objects.filter(recipe_id=obj.recipe_id).count()

class UserMealKitLikeSerializer(serializers.ModelSerializer):
    mealkit = MealKitsSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = MealKitLike
        fields = ['mealkit', 'liked_at', 'likes_count', 'comments_count']

    def get_likes_count(self, obj):
        return MealKitLike.objects.filter(mealkit_id=obj.mealkit_id).count()

    def get_comments_count(self, obj):
        return MealKitComment.objects.filter(mealkit_id=obj.mealkit_id).count()