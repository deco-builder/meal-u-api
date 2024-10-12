from django.db import models
from user_auth.models import User
from community.models import Ingredient, Recipe, MealKit, RecipeIngredient, MealKitRecipe
from groceries.models import Product


class UserCart(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.email}"


class CartProduct(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user_cart", "product")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart for {self.user_cart.user.email}"


class CartMealKit(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    mealkit = models.ForeignKey(MealKit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user_cart", "mealkit")

    def __str__(self):
        return f"{self.quantity} x {self.mealkit.name} in cart for {self.user_cart.user.email}"


class CartRecipe(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    recipe = models.ForeignKey("community.Recipe", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    mealkit = models.ForeignKey(CartMealKit, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ("user_cart", "recipe", "mealkit")

    def __str__(self):
        return f"{self.quantity} x {self.recipe.name} in cart for {self.user_cart.user.email}"


class CartIngredient(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    recipe_ingredient = models.ForeignKey("community.RecipeIngredient", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    recipe = models.ForeignKey(CartRecipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user_cart", "recipe_ingredient", "recipe")

    def __str__(self):
        return f"{self.quantity} x {self.recipe_ingredient} in cart for {self.user_cart.user.email}"


class MealKitRecipeCartRelation(models.Model):
    cart_meal_kit = models.ForeignKey(CartMealKit, on_delete=models.CASCADE)
    cart_recipe = models.ForeignKey(CartRecipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("cart_meal_kit", "cart_recipe")

    def __str__(self):
        return f"MealKit {self.cart_meal_kit.mealkit.name} contains Recipe {self.cart_recipe.recipe.name}"
