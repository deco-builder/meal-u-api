from django.contrib import admin
from .models import UserCart, CartIngredient, CartProduct, CartRecipe, CartMealKit

class CartIngredientInline(admin.TabularInline):
    model = CartIngredient
    extra = 0

class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 0

class CartRecipeInline(admin.TabularInline):
    model = CartRecipe
    extra = 0

class CartMealKitInline(admin.TabularInline):
    model = CartMealKit
    extra = 0

@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    inlines = [CartIngredientInline, CartProductInline, CartRecipeInline, CartMealKitInline]

admin.site.register(CartIngredient)
admin.site.register(CartProduct)
admin.site.register(CartRecipe)
admin.site.register(CartMealKit)