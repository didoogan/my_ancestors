from rest_framework import serializers

from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, write_only=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'
