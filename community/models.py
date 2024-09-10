from django.db import models
from user_auth.models import User
from groceries.models import Ingredients, Units


class MealType(models.Model):
    name = models.CharField(max_length=255)

class Recipes(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    meal_type = models.ForeignKey(MealType, on_delete=models.PROTECT)
    cooking_time = models.PositiveIntegerField()
    instructions = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    photo = models.URLField()
    is_customized = models.BooleanField(default=False)

class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    quantity = models.DecimalField(max_digits=2, decimal_places=2, null=False, blank=False)
    unit = models.ForeignKey(Units, null=False, blank=False, on_delete=models.RESTRICT)

class MealKits(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    photo = models.URLField()
    description = models.TextField()

class MealKitRecipes(models.Model):
    mealkit = models.ForeignKey(MealKits, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('mealkit', 'recipe')

    quantity = models.PositiveIntegerField(default=0)

class IngredientLikes(models.Model):
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    liked_at = models.DateTimeField(auto_now_add=True)

class IngredientComments(models.Model):
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    commented_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=False, blank=False)

class IngredientSaves(models.Model):
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    saved_at = models.DateTimeField(auto_now_add=True)

class IngredientPurchases(models.Model):
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    purchased_at = models.DateTimeField(auto_now_add=True)

class RecipeLikes(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    liked_at = models.DateTimeField(auto_now_add=True)

class RecipeComments(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    commented_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=False, blank=False)

class RecipeSaves(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    saved_at = models.DateTimeField(auto_now_add=True)

class RecipePurchases(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    purchased_at = models.DateTimeField(auto_now_add=True)

class MealKitLikes(models.Model):
    mealkit = models.ForeignKey(MealKits, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    liked_at = models.DateTimeField(auto_now_add=True)

class MealKitComments(models.Model):
    mealkit = models.ForeignKey(MealKits, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    commented_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=False, blank=False)

class MealKitSaves(models.Model):
    mealkit = models.ForeignKey(MealKits, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    saved_at = models.DateTimeField(auto_now_add=True)

class MealKitPurchases(models.Model):
    mealkit = models.ForeignKey(MealKits, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    purchased_at = models.DateTimeField(auto_now_add=True)