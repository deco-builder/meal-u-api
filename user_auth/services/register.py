from ..serializers.register import RegisterSerializer


class RegisterService:
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return "User registered successfully"

            raise Exception(serializer.errors)

        except Exception as e:
            raise e
