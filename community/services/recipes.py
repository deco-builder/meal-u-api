from django.db.models import Q, Count
from ..models import Recipe, RecipeIngredient, DietaryDetail, RecipeLike
from ..serializers.recipes import RecipesSerializer, TrendingRecipesSerializer, TopCreatorSerializer
from .like_and_comment import RecipeLikeAndCommentService


class RecipesService:
    def get(self, dietary_details=None, search=None, creator=None):
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

            if creator:
                queryset = queryset.filter(creator_id=creator).distinct()

            recipes = queryset.order_by("name").all().distinct()
            serializer = RecipesSerializer(recipes, many=True)
            return serializer.data
        except Exception as e:
            raise e

    def get_with_stats(self, user=None, dietary_details=None, search=None):
        """
        Fetch recipes with dietary details, likes, and comments stats for the community page.
        """
        try:
            queryset = (
                Recipe.objects.select_related("meal_type", "creator")
                .prefetch_related(
                    "recipedietarydetail_set__dietary_details",
                    "recipeingredient_set__ingredient",
                    "recipeingredient_set__preparation_type",
                )
                .annotate(
                    likes_count=Count("recipelike"),  # Assuming a related name 'recipelike' in your RecipeLike model
                    comments_count=Count(
                        "recipecomment"
                    ),  # Assuming a related name 'recipecomment' in your RecipeComment model
                )
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
                        recipe_ingredient.preparation_type.additional_price
                        if recipe_ingredient.preparation_type
                        else 0
                    )
                    total_price += ingredient_price + preparation_price

                try:
                    is_like = RecipeLike.objects.get(recipe=recipe.id, user=user)
                except RecipeLike.DoesNotExist:
                    is_like = None

                recipe_data = {
                    "id": recipe.id,
                    "creator": {
                        "name": f"{recipe.creator.first_name} {recipe.creator.last_name}",
                        "profile_picture": recipe.creator.image.url if recipe.creator.image else None,
                        "id": recipe.creator.id
                    },
                    "name": recipe.name,
                    "description": recipe.description,
                    "serving_size": recipe.serving_size,
                    "meal_type": recipe.meal_type.name,
                    "cooking_time": recipe.cooking_time,
                    "created_at": recipe.created_at,
                    "image": recipe.image.url if recipe.image else None,
                    "dietary_details": recipe.recipedietarydetail_set.values_list("dietary_details__name", flat=True),
                    "total_price": total_price,
                    "likes_count": recipe.likes_count,
                    "comments_count": recipe.comments_count,
                    "is_like": False if is_like == None else True
                }
                recipes_with_stats.append(recipe_data)

            return recipes_with_stats
        except Exception as e:
            raise e

    def get_trending_recipes(self):
        try:
            queryset = (
                Recipe.objects.annotate(likes_count=Count("recipelike"), comments_count=Count("recipecomment"))
                .filter(likes_count__gt=0)
                .order_by("-likes_count", "-comments_count")[:7]
            )

            serializer = TrendingRecipesSerializer(queryset, many=True)
            return serializer.data
        except Exception as e:
            raise e

    def get_top_creators_by_recipe_count(self, dietary_detail_id):
        filtered_recipes = Recipe.objects.filter(recipedietarydetail__dietary_details_id=dietary_detail_id)

        top_creators = (
            filtered_recipes.values(
                "creator__id", "creator__email", "creator__first_name", "creator__last_name"
            )
            .annotate(recipe_count=Count("id"))
            .order_by("-recipe_count")
        )

        serializer = TopCreatorSerializer(top_creators, many=True)
        return serializer.data
    
    def get_top_creators_by_dietary_details(self):
        all_dietary_details = DietaryDetail.objects.all()

        top_creators = []

        for dietary_detail in all_dietary_details:
            top_creators_for_detail = self.get_top_creators_by_recipe_count(dietary_detail.id)
            
            if top_creators_for_detail:
                top_creator = top_creators_for_detail[0]  
                top_creators.append({
                    "dietary_detail": {
                        "id": dietary_detail.id,
                        "name": dietary_detail.name,
                    },
                    "top_creator": top_creator
                })

        return top_creators

