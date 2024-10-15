from rest_framework import serializers
from ..models import MealKit, MealkitDietaryDetail, MealKitRecipe


class MealKitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealKit
        fields = "__all__"

class MealKitDietaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealkitDietaryDetail
        fields = "__all__"

class MealKitRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealKitRecipe
        fields = "__all__"