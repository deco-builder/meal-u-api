from django.db import models
from user_auth.models import User
from groceries.models import Unit, Product, DietaryDetail


class Ingredient(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT, null=False, blank=False)
    unit_id = models.ForeignKey(Unit, on_delete=models.PROTECT, null=False, blank=False)
    unit_size = models.DecimalField(
        decimal_places=2, max_digits=6, null=False, blank=False, help_text="Size of the product"
    )
    price_per_unit = models.DecimalField(decimal_places=2, max_digits=6, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.unit_size) + str(self.unit_id) + " " + self.name


class PreparationType(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    additional_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.name + " " + str(self.ingredient)


class MealType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    serving_size = models.PositiveIntegerField()
    meal_type = models.ForeignKey(MealType, on_delete=models.PROTECT)
    cooking_time = models.PositiveIntegerField()
    instructions = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    photo = models.URLField(null=True, blank=True)
    is_customized = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    preparation_type = models.ForeignKey(PreparationType, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("recipe", "ingredient", "preparation_type")

    def __str__(self):
        if self.preparation_type:
            return str(self.preparation_type) + " " + str(self.recipe)
        return str(self.ingredient) + " " + str(self.recipe)


class RecipeDietaryDetail(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    dietary_details = models.ForeignKey(DietaryDetail, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("recipe", "dietary_details")

    def __str__(self):
        return str(self.dietary_details) + " " + str(self.recipe)


class MealKit(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    photo = models.URLField(null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_customized = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MealKitRecipe(models.Model):
    mealkit = models.ForeignKey(MealKit, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("mealkit", "recipe")

    def __str__(self):
        return str(self.mealkit) + " " + str(self.recipe)
    
class MealkitDietaryDetail(models.Model):
    mealkit = models.ForeignKey(MealKit, on_delete=models.CASCADE)
    dietary_details = models.ForeignKey(DietaryDetail, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("mealkit", "dietary_details")

    def __str__(self):
        return str(self.dietary_details) + " " + str(self.recipe)


class IngredientLike(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    liked_at = models.DateTimeField(auto_now_add=True)


class IngredientComment(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    commented_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=False, blank=False)


class IngredientSave(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    saved_at = models.DateTimeField(auto_now_add=True)


class IngredientPurchase(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    purchased_at = models.DateTimeField(auto_now_add=True)


class RecipeLike(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    liked_at = models.DateTimeField(auto_now_add=True)


class RecipeComment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    commented_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=False, blank=False)


class RecipeSave(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    saved_at = models.DateTimeField(auto_now_add=True)


class RecipePurchase(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    purchased_at = models.DateTimeField(auto_now_add=True)


class MealKitLike(models.Model):
    mealkit = models.ForeignKey(MealKit, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    liked_at = models.DateTimeField(auto_now_add=True)


class MealKitComment(models.Model):
    mealkit = models.ForeignKey(MealKit, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    commented_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=False, blank=False)


class MealKitSave(models.Model):
    mealkit = models.ForeignKey(MealKit, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    saved_at = models.DateTimeField(auto_now_add=True)


class MealKitPurchase(models.Model):
    mealkit = models.ForeignKey(MealKit, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    purchased_at = models.DateTimeField(auto_now_add=True)
