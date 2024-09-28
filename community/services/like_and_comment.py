from ..models import RecipeLike, RecipeComment, MealKitLike, MealKitComment, MealKitSave
from ..serializers import RecipeLikeSerializer, RecipeCommentSerializer, MealKitLikeSerializer, MealKitCommentSerializer, MealKitSaveSerializer
from rest_framework.exceptions import ValidationError

class RecipeLikeAndCommentService:

    @staticmethod
    def like_recipe(user, recipe):
        data = {'user': user.id, 'recipe': recipe.id}
        serializer = RecipeLikeSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            like = serializer.save()
            return like

    @staticmethod
    def comment_on_recipe(user, recipe, comment_text):
        data = {'user': user.id, 'recipe': recipe.id, 'comment': comment_text}
        serializer = RecipeCommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            comment = serializer.save()
            return comment

class MealKitLikeAndCommentService:

    @staticmethod
    def like_mealkit(user, mealkit):
        data = {'user': user.id, 'mealkit': mealkit.id}
        serializer = MealKitLikeSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            like = serializer.save()
            return like

    @staticmethod
    def comment_on_mealkit(user, mealkit, comment_text):
        data = {'user': user.id, 'mealkit': mealkit.id, 'comment': comment_text}
        serializer = MealKitCommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            comment = serializer.save()
            return comment

    @staticmethod
    def save_mealkit(user, mealkit):
        data = {'user': user.id, 'mealkit': mealkit.id}
        serializer = MealKitSaveSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            save = serializer.save()
            return save
