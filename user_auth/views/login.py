from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from applibs.response import prepare_success_response, prepare_error_response
from ..services.login import LoginService


class LoginView(APIView):
    def __init__(self):
        self.login_service = LoginService()

    def post(self, request):
        try:
            response = self.login_service.post(request=request)
            return Response(
                prepare_success_response(response), status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                prepare_error_response(str(e)), status=status.HTTP_400_BAD_REQUEST
            )
