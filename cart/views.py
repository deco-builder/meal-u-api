from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from applibs.response import prepare_success_response, prepare_error_response
from .services import CartService

class CartView(APIView):
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
                item_id = request.data.get('recipe_id')
            elif item_type == 'recipe_ingredient':
                item_id = {
                    'recipe_id': request.data.get('recipe_id'),
                    'ingredient_id': request.data.get('ingredient_id'),
                    'preparation_type_id': request.data.get('preparation_type_id')
                }
            elif item_type == 'product':
                item_id = request.data.get('product_id')
            else:
                return Response(prepare_error_response("Invalid item type"), status=status.HTTP_400_BAD_REQUEST)

            response = self.cart_service.add_item(request.user, item_type, item_id, quantity)
            return Response(prepare_success_response(response), status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(prepare_error_response(f"An unexpected error occurred: {str(e)}"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            item_type = request.data.get('item_type')
            
            if item_type == 'recipe':
                item_id = request.data.get('recipe_id')
            elif item_type == 'recipe_ingredient':
                item_id = request.data.get('cart_ingredient_id')  # Assuming you have this ID
            elif item_type == 'product':
                item_id = request.data.get('cart_product_id')  # Assuming you have this ID
            else:
                return Response(prepare_error_response("Invalid item type"), status=status.HTTP_400_BAD_REQUEST)

            response = self.cart_service.remove_item(request.user, item_type, item_id)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(prepare_error_response(f"An unexpected error occurred: {str(e)}"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            item_type = request.data.get('item_type')
            new_quantity = request.data.get('quantity')

            if item_type == 'recipe_ingredient':
                item_id = request.data.get('cart_ingredient_id')  # Assuming you have this ID
            elif item_type == 'product':
                item_id = request.data.get('cart_product_id')  # Assuming you have this ID
            else:
                return Response(prepare_error_response("Invalid item type"), status=status.HTTP_400_BAD_REQUEST)

            response = self.cart_service.update_item_quantity(request.user, item_type, item_id, new_quantity)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(prepare_error_response(f"An unexpected error occurred: {str(e)}"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)