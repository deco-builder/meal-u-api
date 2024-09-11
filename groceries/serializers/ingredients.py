from rest_framework import serializers
from ..models import Ingredient, IngredientDietaryDetail, DietaryDetail


class DietaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietaryDetail
        fields = ["name"]


class IngredientDietaryDetailSerializer(serializers.ModelSerializer):
    dietary_details = serializers.StringRelatedField(source="dietary_details.name")

    class Meta:
        model = IngredientDietaryDetail
        fields = ["dietary_details"]


class IngredientsSerializer(serializers.ModelSerializer):
    category_id = serializers.StringRelatedField()
    unit_id = serializers.StringRelatedField()
    dietary_details = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = "__all__"

    def get_dietary_details(self, obj):
        return obj.ingredientdietarydetail_set.values_list(
            "dietary_details__name", flat=True
        )
