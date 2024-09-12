from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user_auth.models import User
from community.models import Ingredient, Recipe
from groceries.models import Product
from .models import UserCart, CartIngredient, CartProduct, CartRecipe
from unittest.mock import patch, MagicMock

class CartAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = MagicMock(spec=User)
        self.user.email = 'testuser@example.com'
        self.client.force_authenticate(user=self.user)
        
        self.ingredient = {'id': 1, 'name': 'Test Ingredient'}
        self.product = {'id': 1, 'name': 'Test Product'}
        self.recipe = {'id': 1, 'name': 'Test Recipe'}

        self.cart_url = reverse('Cart')

    @patch('cart.services.CartService.get_cart')
    def test_get_cart(self, mock_get_cart):
        mock_get_cart.return_value = {
            'cart_ingredients': [],
            'cart_products': [],
            'cart_recipes': []
        }
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('cart_ingredients', response.data['data'])
        self.assertIn('cart_products', response.data['data'])
        self.assertIn('cart_recipes', response.data['data'])

    @patch('cart.services.CartService.add_item')
    def test_add_ingredient_to_cart(self, mock_add_item):
        mock_add_item.return_value = {'id': 1, 'ingredient': self.ingredient, 'quantity': 2}
        data = {
            'item_type': 'ingredient',
            'item_id': self.ingredient['id'],
            'quantity': 2
        }
        response = self.client.post(self.cart_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_add_item.assert_called_once()

    @patch('cart.services.CartService.add_item')
    def test_add_product_to_cart(self, mock_add_item):
        mock_add_item.return_value = {'id': 1, 'product': self.product, 'quantity': 1}
        data = {
            'item_type': 'product',
            'item_id': self.product['id'],
            'quantity': 1
        }
        response = self.client.post(self.cart_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_add_item.assert_called_once()

    @patch('cart.services.CartService.add_item')
    def test_add_recipe_to_cart(self, mock_add_item):
        mock_add_item.return_value = {'id': 1, 'recipe': self.recipe, 'quantity': 1}
        data = {
            'item_type': 'recipe',
            'item_id': self.recipe['id'],
            'quantity': 1
        }
        response = self.client.post(self.cart_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_add_item.assert_called_once()

    @patch('cart.services.CartService.remove_item')
    def test_remove_item_from_cart(self, mock_remove_item):
        mock_remove_item.return_value = None
        data = {
            'item_type': 'ingredient',
            'item_id': 1
        }
        response = self.client.delete(self.cart_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_remove_item.assert_called_once()

    @patch('cart.services.CartService.update_item_quantity')
    def test_update_item_quantity(self, mock_update_quantity):
        mock_update_quantity.return_value = {'id': 1, 'product': self.product, 'quantity': 3}
        data = {
            'item_type': 'product',
            'item_id': 1,
            'quantity': 3
        }
        response = self.client.put(self.cart_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_update_quantity.assert_called_once()