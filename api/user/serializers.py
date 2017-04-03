from rest_framework import serializers

from django.contrib.auth import get_user_model


class UserSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

