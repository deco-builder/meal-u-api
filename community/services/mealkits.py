from ..models import MealKit, Recipe
from ..serializers.mealkits import MealKitsSerializer, CommunityMealKitsSerializer
from ..serializers.recipes import RecipesSerializer
from django.db.models import Q, Count


class MealKitsServices:
    def get(self, dietary_details=None, search=None, creator=None):
        try:
            queryset = MealKit.objects.prefetch_related("mealkitdietarydetail_set__dietary_details")
            

            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search)
                    | Q(description__icontains=search)
                    | Q(mealkitrecipe__recipe__recipeingredient__ingredient__product_id__name__icontains=search)
                    | Q(mealkitrecipe__recipe__recipeingredient__ingredient__product_id__description__icontains=search)
                    | Q(
                        mealkitrecipe__recipe__recipeingredient__ingredient__product_id__category_id__name__icontains=search
                    )
                ).distinct()

            if dietary_details:
                queryset = queryset.filter(mealkitdietarydetail__dietary_details__name__in=dietary_details).distinct()
            
            if creator:
                queryset = queryset.filter(creator_id=creator).distinct()

            mealkits = queryset.order_by("name").all().distinct()
            serializer = MealKitsSerializer(mealkits, many=True)
            return serializer.data
        except Exception as e:
            raise e
    
    def get_trending_mealkits(self):
        try:
            queryset = MealKit.objects.annotate(
                likes_count=Count('mealkitlike'),
                comments_count=Count('mealkitcomment')
            ).filter(likes_count__gt=0).order_by('-likes_count', '-comments_count')[:7]  
        
            serializer = MealKitsSerializer(queryset, many=True)
            return serializer.data
        except Exception as e:
            raise e
    
    def get_with_stats(self):
        try:
            queryset = MealKit.objects.prefetch_related("mealkitdietarydetail_set__dietary_details").annotate(
                likes_count=Count('mealkitlike'),
                comments_count=Count('mealkitcomment') 
            )

            mealkits = queryset.order_by("name").all().distinct()
            serializer = CommunityMealKitsSerializer(mealkits, many=True)
            return serializer.data
        except Exception as e:
            raise e

class CombinedService:
    def get_combined_mealkits_and_recipes(self):
        try:
            # Fetch meal kits and recipes
            meal_kits = MealKit.objects.all()
            recipes = Recipe.objects.all()

            # Serialize both meal kits and recipes
            meal_kit_serializer = MealKitsSerializer(meal_kits, many=True)
            recipe_serializer = RecipesSerializer(recipes, many=True)

            # Combine both serialized data into a single list
            combined_data = meal_kit_serializer.data + recipe_serializer.data

            # Sort the combined data by 'created_at' in descending order
            sorted_data = sorted(combined_data, key=lambda x: x['created_at'], reverse=True)

            return sorted_data
        except Exception as e:
            raise e