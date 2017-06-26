from rest_framework import serializers

from ancestors.models import Ancestor
from api.user.serializers import UserSerializer


class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Ancestor
        fields = ('id', 'user', 'birth', 'death', 'bio', 'first_name',
                  'last_name', 'third_name')


class AncestorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    parents = ParentSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Ancestor
        # fields = ('id', 'user', 'parents', 'birth', 'death', 'bio',
        #           'first_name', 'last_name', 'third_name')
        fields = '__all__'
