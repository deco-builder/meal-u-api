from django.db.models import Q, Count
from ..models import Recipe, RecipeIngredient
from ..serializers.recipes import RecipesSerializer
from .like_and_comment import RecipeLikeAndCommentService


class RecipesService:
    def get(self, dietary_details=None, search=None):
        try:
            queryset = Recipe.objects.select_related("meal_type").prefetch_related(
                "recipedietarydetail_set__dietary_details",
                "recipeingredient_set__ingredient",
                "recipeingredient_set__preparation_type",
            )

            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search)
                    | Q(description__icontains=search)
                    | Q(recipeingredient__ingredient__product_id__name__icontains=search)
                    | Q(recipeingredient__ingredient__product_id__description__icontains=search)
                    | Q(recipeingredient__ingredient__product_id__category_id__name__icontains=search)
                ).distinct()

            if dietary_details:
                queryset = queryset.filter(recipedietarydetail__dietary_details__name__in=dietary_details).distinct()

            recipes = queryset.order_by("name").all().distinct()
            serializer = RecipesSerializer(recipes, many=True)
            return serializer.data
        except Exception as e:
            raise e

    def get_with_stats(self, dietary_details=None, search=None):
        """
        Fetch recipes with dietary details, likes, and comments stats for the community page.
        """
        try:
            queryset = Recipe.objects.select_related("meal_type", "creator").prefetch_related(
                "recipedietarydetail_set__dietary_details",
                "recipeingredient_set__ingredient",
                "recipeingredient_set__preparation_type",
            ).annotate(
                likes_count=Count('recipelike'),  # Assuming a related name 'recipelike' in your RecipeLike model
                comments_count=Count('recipecomment')  # Assuming a related name 'recipecomment' in your RecipeComment model
            )

            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search)
                    | Q(description__icontains=search)
                    | Q(recipeingredient__ingredient__product_id__name__icontains=search)
                    | Q(recipeingredient__ingredient__product_id__description__icontains=search)
                    | Q(recipeingredient__ingredient__product_id__category_id__name__icontains=search)
                )

            if dietary_details:
                queryset = queryset.filter(recipedietarydetail__dietary_details__name__in=dietary_details).distinct()

            recipes_with_stats = []
            for recipe in queryset:
                total_price = 0
                recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
                for recipe_ingredient in recipe_ingredients:
                    ingredient_price = recipe_ingredient.ingredient.price_per_unit
                    preparation_price = (
                        recipe_ingredient.preparation_type.additional_price if recipe_ingredient.preparation_type else 0
                    )
                    total_price += ingredient_price + preparation_price
                recipe_data = {
                    'id': recipe.id,
                    'creator': {
                        'name': f"{recipe.creator.first_name} {recipe.creator.last_name}",
                        'profile_picture': recipe.creator.image.url if recipe.creator.image else None,
                    },
                    'name': recipe.name,
                    'serving_size': recipe.serving_size,
                    'meal_type': recipe.meal_type.name,
                    'cooking_time': recipe.cooking_time,
                    'created_at': recipe.created_at,
                    'image': recipe.image.url if recipe.image else None,
                    'dietary_details': recipe.recipedietarydetail_set.values_list('dietary_details__name', flat=True),
                    'total_price': total_price,
                    'likes_count': recipe.likes_count,
                    'comments_count': recipe.comments_count
                }
                recipes_with_stats.append(recipe_data)

            return recipes_with_stats
        except Exception as e:
            raise e