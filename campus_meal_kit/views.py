from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from applibs.response import prepare_success_response, prepare_error_response


class HomeView(APIView):
    def get(self, request):
        return Response(
            prepare_success_response("Hello World!"), status=status.HTTP_200_OK
        )
