from ..models import RecipeLike, RecipeComment, MealKitLike, MealKitComment, MealKitSave
from ..serializers.like_and_comment import RecipeLikeSerializer, RecipeCommentSerializer, MealKitLikeSerializer, MealKitCommentSerializer, UserRecipeLikeSerializer, UserMealKitLikeSerializer
from rest_framework.exceptions import ValidationError

LIKE_THRESHOLD = 5
COMMENT_THRESHOLD = 1

class RecipeLikeAndCommentService:

    @staticmethod
    def like_recipe(user, recipe):
        try:
            existing_like = RecipeLike.objects.get(user=user, recipe=recipe)
            existing_like.delete()
            message = 'Like removed'
        except RecipeLike.DoesNotExist:
            data = {'user': user.id, 'recipe': recipe.id}
            serializer = RecipeLikeSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                like = serializer.save()
                message = 'Like added'

        RecipeLikeAndCommentService.check_and_update_monetization(recipe)

        return {'message': message}

    @staticmethod
    def check_and_update_monetization(recipe):

        likes_count = RecipeLike.objects.filter(recipe=recipe).count()
        comments_count = RecipeComment.objects.filter(recipe=recipe).count()

        if likes_count >= LIKE_THRESHOLD and comments_count >= COMMENT_THRESHOLD:
            recipe.monetize = True
            recipe.save()
        else:
            recipe.monetize = False
            recipe.save()

    @staticmethod
    def comment_on_recipe(user, recipe, comment_text):
        data = {'user': user.id, 'recipe': recipe.id, 'comment': comment_text}
        serializer = RecipeCommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            comment = serializer.save()
            RecipeLikeAndCommentService.check_and_update_monetization(recipe)
            return comment
    
    @staticmethod
    def get_recipe_likes_count(recipe_id):
        return RecipeLike.objects.filter(recipe_id=recipe_id).count()

    @staticmethod
    def get_recipe_comments_count(recipe_id):
        return RecipeComment.objects.filter(recipe_id=recipe_id).count()

    @staticmethod
    def get_all_recipe_comments(recipe_id):
        return RecipeComment.objects.filter(recipe_id=recipe_id).order_by('-commented_at')
    

class MealKitLikeAndCommentService:

    @staticmethod
    def like_mealkit(user, mealkit):
        try:
            existing_like = MealKitLike.objects.get(user=user, mealkit=mealkit)
            existing_like.delete()
            message= 'Like removed'
        except MealKitLike.DoesNotExist:
            data = {'user': user.id, 'mealkit': mealkit.id}
            serializer = MealKitLikeSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                like = serializer.save()
            message= 'Like added'

        
        MealKitLikeAndCommentService.check_and_update_monetization(mealkit)

        return {'message': message}


    @staticmethod
    def check_and_update_monetization(mealkit):

        likes_count = MealKitLike.objects.filter(mealkit=mealkit).count()
        comments_count = MealKitComment.objects.filter(mealkit=mealkit).count()

        if likes_count >= LIKE_THRESHOLD and comments_count >= COMMENT_THRESHOLD:
            mealkit.monetize = True
            mealkit.save()
        else:
            mealkit.monetize = False
            mealkit.save()

    @staticmethod
    def comment_on_mealkit(user, mealkit, comment_text):
        data = {'user': user.id, 'mealkit': mealkit.id, 'comment': comment_text}
        serializer = MealKitCommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            comment = serializer.save()
            return comment
    
    @staticmethod
    def get_mealkit_likes_count(mealkit_id):
        return MealKitLike.objects.filter(mealkit_id=mealkit_id).count()

    @staticmethod
    def get_mealkit_comments_count(mealkit_id):
        return MealKitComment.objects.filter(mealkit_id=mealkit_id).count()

    @staticmethod
    def get_all_mealkit_comments(mealkit_id):
        return MealKitComment.objects.filter(mealkit_id=mealkit_id).order_by('-commented_at')


class LikeService:
    @staticmethod
    def get_user_likes(user):
        liked_recipes = RecipeLike.objects.filter(user=user).select_related('recipe')
        liked_mealkits = MealKitLike.objects.filter(user=user).select_related('mealkit')
        liked_recipes_serializer = UserRecipeLikeSerializer(liked_recipes, many=True)
        liked_mealkits_serializer = UserMealKitLikeSerializer(liked_mealkits, many=True)

        return liked_recipes_serializer, liked_mealkits_serializer