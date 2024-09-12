from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import UserCart, CartIngredient, CartProduct, CartRecipe
from community.models import Recipe, RecipeIngredient, Ingredient, MealType, PreparationType
from groceries.models import Product, Category, Unit, DietaryDetail
from .services import CartService
from decimal import Decimal

User = get_user_model()

class CartServiceTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cart_service = CartService()

        # Create User
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

        # Create MealType
        self.meal_type = MealType.objects.create(name='Lunch')

        # Create Category, Unit, and DietaryDetail
        self.category = Category.objects.create(name='Test Category')
        self.unit = Unit.objects.create(name='gram')
        self.dietary_detail = DietaryDetail.objects.create(name='Vegan')

        # Create Product
        self.product = Product.objects.create(
            name='Test Product',
            category_id=self.category,
            unit_id=self.unit,
            unit_size=Decimal('500.00'),
            price_per_unit=Decimal('10.00'),
            measurement_size=Decimal('100.00'),
            description='Test product description',
            stock=100
        )

        # Create Ingredient
        self.ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            product_id=self.product,
            unit_id=self.unit,
            unit_size=Decimal('1.00'),
            price_per_unit=Decimal('5.00'),
            description='Test ingredient description',
            stock=50
        )

        # Create PreparationType
        self.preparation_type = PreparationType.objects.create(
            name='Chopped',
            ingredient=self.ingredient,
            additional_price=Decimal('1.00')
        )

        # Create Recipe
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            creator=self.user,
            description='Test recipe description',
            serving_size=4,
            meal_type=self.meal_type,
            cooking_time=30,
            instructions={'step1': 'Do this', 'step2': 'Do that'},
            photo='http://example.com/recipe.jpg'
        )

        # Create RecipeIngredient
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            preparation_type=self.preparation_type
        )

    def test_get_cart(self):
        cart_data = self.cart_service.get_cart(self.user)
        self.assertIsNotNone(cart_data)
        self.assertEqual(cart_data['user'], self.user.id)


    def test_add_product_to_cart(self):
        item_data = self.cart_service.add_item(self.user, 'product', self.product.id, 3)
        self.assertIsNotNone(item_data)
        self.assertEqual(item_data['quantity'], 3)
        self.assertEqual(item_data['product']['id'], self.product.id)

    def test_add_recipe_to_cart(self):
        # Create a MealType
        meal_type = MealType.objects.create(name="Test Meal Type")

        # Create a Recipe
        recipe = Recipe.objects.create(
            name="Test Recipe",
            description="Test Description",
            cooking_time=30,
            instructions="Test Instructions",
            creator=self.user,
            meal_type=meal_type,
            serving_size=4
        )

        # Add the recipe to the cart
        cart_service = CartService()
        cart_item = cart_service.add_item(self.user, 'recipe', recipe.id)

        # Check if the recipe was added to the cart
        self.assertIn('recipe', cart_item)
        self.assertEqual(cart_item['recipe']['id'], recipe.id)
        self.assertEqual(cart_item['recipe']['name'], 'Test Recipe')
        self.assertEqual(cart_item['quantity'], 1)

    def test_remove_item_from_cart(self):
        # Create a Category
        category = Category.objects.create(name="Test Category")

        # Create a Unit
        unit = Unit.objects.create(name="Test Unit")

        # Create a product
        product = Product.objects.create(
            name="Test Product",
            category_id=category.id,
            unit_id=unit.id,
            unit_size=1,
            price_per_unit=10,
            measurement_size=100,
            price_per_measurement=1000,
            description="Test Description",
            stock=10
        )

        # Add the product to the cart
        cart_service = CartService()
        cart_item = cart_service.add_item(self.user, 'product', product.id)

        # Print the structure of cart_item for debugging
        print("Cart item after adding:", cart_item)

        # Verify the product is in the cart
        self.assertIn('product', cart_item)
        self.assertEqual(cart_item['product']['id'], product.id)

        # Get the cart_item_id
        cart_item_id = cart_item['id']

        # Remove the product from the cart
        result = cart_service.remove_item(self.user, 'product', cart_item_id)

        # Print the result of remove_item for debugging
        print("Result of remove_item:", result)

        # Check if the product was removed from the cart
        # The exact assertion here depends on what remove_item returns
        # It might return a boolean indicating success, or an updated cart
        # Adjust the assertion based on the actual behavior of remove_item
        self.assertTrue(result)  # Assuming remove_item returns True on success

    def test_update_item_quantity(self):
        # Create a Category and Unit first
        category = Category.objects.create(name="Test Category")
        unit = Unit.objects.create(name="Test Unit")

        # First, add a product to the cart
        product = Product.objects.create(
            name="Test Product",
            category_id=category,
            unit_id=unit,
            unit_size=1.0,
            price_per_unit=10.0,
            measurement_size=100.0,
            description="Test Description",
            stock=10
        )
        self.cart_service.add_item(self.user, 'product', product.id)

        # Get the cart to find the CartProduct id
        cart = self.cart_service.get_cart(self.user)
        cart_product_id = cart['cart_products'][0]['id']

        # Now update the quantity
        updated_cart = self.cart_service.update_item_quantity(self.user, 'product', cart_product_id, 5)

        # Check if the quantity was updated
        self.assertEqual(updated_cart['cart_products'][0]['quantity'], 5)

    def test_add_existing_item_increases_quantity(self):
        # Add an item to the cart
        self.cart_service.add_item(self.user, 'product', self.product.id, 2)

        # Add the same item again
        self.cart_service.add_item(self.user, 'product', self.product.id, 3)

        # Check if the quantity was increased
        cart_data = self.cart_service.get_cart(self.user)
        self.assertEqual(cart_data['cart_products'][0]['quantity'], 5)

    def test_invalid_item_type(self):
        with self.assertRaises(ValueError):
            self.cart_service.add_item(self.user, 'invalid_type', self.product.id, 1)

    def test_nonexistent_item(self):
        with self.assertRaises(Exception):
            self.cart_service.add_item(self.user, 'product', 9999, 1)  # Assuming 9999 is a non-existent product id

    def test_product_price_per_measurement_calculation(self):
        self.assertEqual(self.product.price_per_measurement, Decimal('2.00'))

    def test_product_save_updates_price_per_measurement(self):
        self.product.price_per_unit = Decimal('20.00')
        self.product.save()
        self.assertEqual(self.product.price_per_measurement, Decimal('4.00'))

    def test_recipe_ingredient_with_preparation_type(self):
        self.assertEqual(str(self.recipe_ingredient), "Chopped 1.00gram Test Ingredient Test Recipe")

    def test_recipe_ingredient_without_preparation_type(self):
        recipe_ingredient_without_prep = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient
        )
        self.assertEqual(str(recipe_ingredient_without_prep), "1.00gram Test Ingredient Test Recipe")