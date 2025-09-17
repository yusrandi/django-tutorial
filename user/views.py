from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer


# Create your views here.
class UserView(ViewSet):
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
