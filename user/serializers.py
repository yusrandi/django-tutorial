from rest_framework import serializers
from .models import User


# Create your serializers here.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "password"]
        read_only_fields = ["id"]
