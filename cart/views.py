from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from applibs.response import prepare_success_response, prepare_error_response
from .services import CartService


class CartView(APIView):
    def __init__(self):
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
            item_id = request.data.get('item_id')
            quantity = request.data.get('quantity', 1)
            recipe_id = request.data.get('recipe_id')

            response = self.cart_service.add_item(request.user, item_type, item_id, quantity, recipe_id)
            return Response(prepare_success_response(response), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            item_type = request.data.get('item_type')
            item_id = request.data.get('item_id')

            self.cart_service.remove_item(request.user, item_type, item_id)
            return Response(prepare_success_response("Item removed successfully"), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            item_type = request.data.get('item_type')
            item_id = request.data.get('item_id')
            new_quantity = request.data.get('quantity')

            response = self.cart_service.update_item_quantity(request.user, item_type, item_id, new_quantity)
            return Response(prepare_success_response(response), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST)