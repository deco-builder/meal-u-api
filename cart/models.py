from django.db import models
from user_auth.models import User
from community.models import Ingredient, Recipe, MealKit
from groceries.models import Product

class UserCart(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.email}"

class CartIngredient(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name='cart_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('user_cart', 'ingredient', 'recipe')

    def __str__(self):
        recipe_name = f" for {self.recipe.name}" if self.recipe else ""
        return f"{self.quantity} x {self.ingredient.name}{recipe_name} in cart for {self.user_cart.user.email}"

class CartProduct(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user_cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart for {self.user_cart.user.email}"

class CartRecipe(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name='cart_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user_cart', 'recipe')

    def __str__(self):
        return f"{self.quantity} x {self.recipe.name} in cart for {self.user_cart.user.email}"

class CartMealKit(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name='cart_mealkits')
    mealkit = models.ForeignKey(MealKit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user_cart', 'mealkit')

    def __str__(self):
        return f"{self.quantity} x {self.mealkit.name} in cart for {self.user_cart.user.email}"