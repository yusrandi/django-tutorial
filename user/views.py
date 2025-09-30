from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# from rest_framework.permissions import IsAuthenticated
# from rest_framework.permissions import IsAdminUser

from .permissions import IsAuthenticatedNonStaff


# Create your views here.
class UserView(ViewSet):
    permission_classes = [IsAuthenticatedNonStaff]

    # GET /api/users/
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(
            {
                "status": "success",
                "status_code": status.HTTP_200_OK,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # POST /api/users/
    def create(self, request):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "status_code": status.HTTP_201_CREATED,
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": "error",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # GET /api/users/<id>/
    def retrieve(self, request, pk=None):
        try:
            book = User.objects.get(pk=pk)
            serializer = UserSerializer(book)
            return Response(
                {
                    "status": "success",
                    "status_code": status.HTTP_200_OK,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": "Book not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    # PUT /api/users/<id>/
    def update(self, request, pk=None):
        try:
            book = User.objects.get(pk=pk)
            serializer = UserSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": "success",
                        "status_code": status.HTTP_200_OK,
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "status": "error",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except User.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": "Book not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    # DELETE /api/users/<id>/
    def destroy(self, request, pk=None):
        try:
            book = User.objects.get(pk=pk)
            book.delete()
            return Response(
                {
                    "status": "success",
                    "status_code": status.HTTP_204_NO_CONTENT,
                    "message": "Book deleted successfully",
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except User.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": "Book not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    # @api_view(["POST"])
    # def register(self, request):
    #     data = request.data
    #     serializer = UserSerializer(data=data)
    #     if serializer.is_valid():
    #         user = User.objects.create_user(
    #             email=data["email"], name=data["name"], password=data["password"]
    #         )
    #         return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @api_view(["POST"])
    # def login(self, request):
    #     email = request.data.get("email")
    #     password = request.data.get("password")
    #     user = authenticate(request, email=email, password=password)

    #     if user is not None:
    #         return Response(
    #             {"message": "Login success", "user": UserSerializer(user).data}
    #         )
    #     else:
    #         return Response(
    #             {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
    #         )


class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                name=serializer.validated_data["name"],
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
                is_active=serializer.validated_data.get("is_active", True),
                is_staff=serializer.validated_data.get("is_staff", False),
            )

            # ini adalah contoh membuat token jwt
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # cek kredensial user
        user = authenticate(request, email=email, password=password)

        if not user:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # buat token jwt
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
