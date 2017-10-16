from rest_framework import serializers

from ancestors.models import Ancestor
from api.photos.serializers import PhotoSerializer
from api.user.serializers import UserSerializer


class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Ancestor
        fields = '__all__'


# class AncestorSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     parents = ParentSerializer(many=True, read_only=True, required=False)
#     children = ParentSerializer(many=True, read_only=True, required=False,
#                                 source='childrens')
#     siblings = ParentSerializer(many=True, read_only=True, required=False)
#     photos = PhotoSerializer(many=True, read_only=True, required=False)
#
#     class Meta:
#         model = Ancestor
#         # fields = ('id', 'user', 'parents', 'birth', 'death', 'bio',
#         #           'first_name', 'last_name', 'third_name')
#         fields = '__all__'

class AncestorSerializer(ParentSerializer):
    children = serializers.PrimaryKeyRelatedField(many=True, required=False,
                            queryset=Ancestor.objects.all())
    siblings = serializers.PrimaryKeyRelatedField(many=True, required=False,
                            queryset=Ancestor.objects.all())
    # parents = serializers.PrimaryKeyRelatedField(many=True, required=False,
    #                         queryset=Ancestor.objects.filter(abstract=False))

    class Meta:
        model = Ancestor
        fields = '__all__'

    def create(self, validated_data):
        siblings = validated_data.pop('siblings', [])
        parents = validated_data.pop('parents', [])
        if not parents:
            for sibling in siblings:
                for parent in sibling.parents.all():
                    parents.append(parent)
        if not parents:
            parents.append(Ancestor.objects.create(abstract=True))
        children = validated_data.pop('children', False)
        user = self.context.get('request').user
        validated_data['user'] = user
        ancestor = Ancestor.objects.create(**validated_data)
        # Children should have the same parents
        siblings.append(ancestor)
        if parents and siblings:
            for sibling in siblings:
                for parent in parents:
                    sibling.parents.add(parent)
        for child in children:
            child.parents.add(ancestor)
        return ancestor
