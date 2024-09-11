from django.db import models
from user_auth.models import User
from groceries.models import Unit, Category

class Ingredient(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT, null=False, blank=False)
    unit_id = models.ForeignKey(Unit, on_delete=models.PROTECT, null=False, blank=False)
    unit_size = models.DecimalField(decimal_places=2, max_digits=6, null=False, blank=False, help_text="Size of the product")
    price_per_unit = models.DecimalField(decimal_places=2, max_digits=6, null=False, blank=False)
    measurement_size = models.DecimalField(decimal_places=2, max_digits=6, null=True, help_text="Size of the measurement unit (e.g., 100 for 100g)")
    price_per_measurement = models.DecimalField(decimal_places=2, max_digits=6, blank=True, help_text="Price for the given measurement size")
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    

    def calculate_price_per_measurement(self):
        if self.unit_size <= 0 or self.measurement_size <= 0:
            return None
        
        return (self.price_per_unit / self.unit_size) * self.measurement_size

    def save(self, *args, **kwargs):
        self.price_per_measurement = self.calculate_price_per_measurement()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MealType(models.Model):
    name = models.CharField(max_length=255)


class Recipe(models.Model):
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


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("recipe", "ingredient")

    quantity = models.DecimalField(
        max_digits=2, decimal_places=2, null=False, blank=False
    )
    unit = models.ForeignKey(Unit, null=False, blank=False, on_delete=models.RESTRICT)


class MealKit(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    photo = models.URLField()
    description = models.TextField()


class MealKitRecipe(models.Model):
    mealkit = models.ForeignKey(MealKit, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("mealkit", "recipe")

    quantity = models.PositiveIntegerField(default=0)


class IngredientLike(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    liked_at = models.DateTimeField(auto_now_add=True)


class IngredientComment(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    commented_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=False, blank=False)


class IngredientSave(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    saved_at = models.DateTimeField(auto_now_add=True)


class IngredientPurchase(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    purchased_at = models.DateTimeField(auto_now_add=True)


class RecipeLike(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    liked_at = models.DateTimeField(auto_now_add=True)


class RecipeComment(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    commented_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=False, blank=False)


class RecipeSave(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    saved_at = models.DateTimeField(auto_now_add=True)


class RecipePurchase(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    purchased_at = models.DateTimeField(auto_now_add=True)


class MealKitLike(models.Model):
    mealkit = models.ForeignKey(
        MealKit, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    liked_at = models.DateTimeField(auto_now_add=True)


class MealKitComment(models.Model):
    mealkit = models.ForeignKey(
        MealKit, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    commented_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=False, blank=False)


class MealKitSave(models.Model):
    mealkit = models.ForeignKey(
        MealKit, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    saved_at = models.DateTimeField(auto_now_add=True)


class MealKitPurchase(models.Model):
    mealkit = models.ForeignKey(
        MealKit, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    purchased_at = models.DateTimeField(auto_now_add=True)
