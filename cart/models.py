from django.db import models
from user_auth.models import User
from community.models import Ingredient, Recipe, MealKit, RecipeIngredient
from groceries.models import Product, PreparationType


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
    recipe = models.ForeignKey(CartRecipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    preparation_type = models.ForeignKey(PreparationType, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user_cart", "recipe", "ingredient", "preparation_type")

    def __str__(self):
        return f"{self.quantity} x {str(self.preparation_type)} {str(self.ingredient)} in cart for {self.user_cart.user.email}"
    
    def save(self, *args, **kwargs):
        if self.preparation_type:
            if self.preparation_type.category != self.ingredient.product_id.category_id:
                raise ValueError(
                    f"The preparation type '{self.preparation_type}' is for product category {self.preparation_type.category}, does not match the product category '{self.ingredient.product_id.category_id}'."
                )

        super().save(*args, **kwargs)
