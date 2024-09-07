from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from applibs.response import prepare_success_response, prepare_error_response
from ..serializers.register import RegisterSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                prepare_success_response({"message": "User registered successfully"}),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            prepare_error_response(serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )
