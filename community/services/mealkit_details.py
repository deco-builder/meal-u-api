import json
from ..models import MealKit, Recipe
from ..serializers.mealkit_details import MealKitDetailsSerializer
from ..serializers.create_mealkit import MealKitSerializer, MealKitDietaryDetailSerializer, MealKitRecipeSerializer
from django.db import transaction


class MealKitDetailsServices:
    def get(self, mealkit_id):
        try:
            mealkit = MealKit.objects.prefetch_related("mealkitdietarydetail_set__dietary_details").get(id=mealkit_id)
            serializer = MealKitDetailsSerializer(mealkit)
            return serializer.data
        except Exception as e:
            raise e

    def post(self, data, user, image):
        try:
            with transaction.atomic():
                mealkit = json.loads(data.get("mealkit", {}))
                mealkit["creator"] = user.id
                mealkit["image"] = image

                mealkit_serializer = MealKitSerializer(data=mealkit)
                mealkit_serializer.is_valid(raise_exception=True)
                mealkit = mealkit_serializer.save()

                recipes = json.loads(data.get("mealkit", {})).get("recipes", [])
                for recipe in recipes:
                    recipe_obj = Recipe.objects.get(id=recipe)
                    if recipe_obj.creator.id != user.id:
                        raise Exception(f"User {str(user)} is not the creator of recipe {str(recipe_obj)}.")
                    
                    mealkit_recipe_data = {"mealkit": mealkit.id, "recipe": recipe}
                    mealkit_recipe_serializer = MealKitRecipeSerializer(data=mealkit_recipe_data)
                    mealkit_recipe_serializer.is_valid(raise_exception=True)
                    mealkit_recipe_serializer.save()

                dietary_details = json.loads(data.get("mealkit", {})).get("dietary_details", [])
                for dietary_detail in dietary_details:
                    dietary_detail_data = {"mealkit": mealkit.id, "dietary_details": dietary_detail}
                    mealkit_dietary_detail_serializer = MealKitDietaryDetailSerializer(data=dietary_detail_data)
                    mealkit_dietary_detail_serializer.is_valid(raise_exception=True)
                    mealkit_dietary_detail_serializer.save()
                
                return self.get(mealkit.id)

        except Exception as e:
            raise e
