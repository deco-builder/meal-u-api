from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from user_auth.permission import IsWarehouseUser, IsClientUser
from applibs.response import prepare_success_response, prepare_error_response
from .services import CartService

class CartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsWarehouseUser | IsClientUser]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart_service = CartService()

    def get(self, request):
        try:
            response = self.cart_service.get_cart(request.user)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            item_type = request.data.get('item_type')
            quantity = request.data.get('quantity', 1)

            if item_type == 'recipe':
                item_data = {
                    'recipe_id': request.data.get('recipe_id'),
                    'recipe_ingredients': request.data.get('recipe_ingredients', [])
                }
            elif item_type == 'product':
                item_data = request.data.get('product_id')
            elif item_type == 'mealkit':
                item_data = request.data.get('item_data', {})
            else:
                return Response(prepare_error_response("Invalid item type"), status=status.HTTP_400_BAD_REQUEST)

            response = self.cart_service.add_item(request.user, item_type, item_data, quantity)
            return Response(prepare_success_response(response), status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(prepare_error_response(f"An unexpected error occurred: {str(e)}"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            item_type = request.data.get('item_type')
            
            if item_type == 'recipe':
                item_id = request.data.get('cart_recipe_id')
            elif item_type == 'recipe_ingredient':
                item_id = request.data.get('cart_ingredient_id')
            elif item_type == 'product':
                item_id = request.data.get('cart_product_id')
            elif item_type == 'mealkit':
                item_id = request.data.get('cart_mealkit_id')
            else:
                return Response(prepare_error_response("Invalid item type"), status=status.HTTP_400_BAD_REQUEST)

            # print(f"item_type: {item_type}, item_id being passed to remove_item: {item_id}")

            if item_id is None:
                return Response(prepare_error_response("Item ID is required"), status=status.HTTP_400_BAD_REQUEST)

            response = self.cart_service.remove_item(request.user, item_type, item_id)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(prepare_error_response(f"An unexpected error occurred: {str(e)}"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            item_type = request.data.get('item_type')
            item_id = request.data.get('item_id')
            new_quantity = request.data.get('quantity')

            if not item_type or not item_id or new_quantity is None:
                return Response(prepare_error_response("Item type, item ID, and quantity are required"), status=status.HTTP_400_BAD_REQUEST)

            if item_type not in ['recipe_ingredient', 'product', 'recipe', 'mealkit']:
                return Response(prepare_error_response("Invalid item type"), status=status.HTTP_400_BAD_REQUEST)

            response = self.cart_service.update_item_quantity(request.user, item_type, item_id, new_quantity)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(prepare_error_response(f"An unexpected error occurred: {str(e)}"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)