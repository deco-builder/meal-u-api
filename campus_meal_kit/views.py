from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from applibs.response import prepare_success_response, prepare_error_response

from .models import Item
from .serializers import ItemSerializer


class HomeView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)

        return Response(
            prepare_success_response(serializer.data), status=status.HTTP_200_OK
        )
