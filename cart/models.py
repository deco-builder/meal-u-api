from django.db import models
from user_auth.models import User
from community.models import Ingredient, Recipe, MealKit, RecipeIngredient, MealKitRecipe
from groceries.models import Product

class UserCart(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.email}"

class CartIngredient(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name='cart_ingredients')
    recipe_ingredient = models.ForeignKey('community.RecipeIngredient', on_delete=models.CASCADE)
    cart_recipe = models.ForeignKey('CartRecipe', on_delete=models.CASCADE, related_name='cart_ingredients', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user_cart', 'recipe_ingredient', 'cart_recipe')

    def __str__(self):
        return f"{self.quantity} x {self.recipe_ingredient} in {self.cart_recipe} for {self.user_cart.user.email}"

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
    meal_kit_recipe = models.ForeignKey(MealKitRecipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='cart_recipes')
    quantity = models.PositiveIntegerField(default=1)
    is_from_mealkit = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user_cart', 'recipe', 'meal_kit_recipe')

    def __str__(self):
        source = "from MealKit" if self.meal_kit_recipe else "directly added"
        return f"{self.quantity} x {self.recipe.name} in cart {source}"
        
class CartMealKit(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name='cart_mealkits')
    mealkit = models.ForeignKey(MealKit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user_cart', 'mealkit')

    def __str__(self):
        return f"{self.quantity} x {self.mealkit.name} in cart for {self.user_cart.user.email}"
