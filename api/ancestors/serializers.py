from rest_framework import serializers

from ancestors.models import Ancestor
from ancestors.tasks import update_ancestors
from api.photos.serializers import PhotoSerializer
from api.user.serializers import UserSerializer


class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Ancestor
        fields = '__all__'


class ParentsPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        if value.abstract is True:
            return
        return super(ParentsPrimaryKeyRelatedField, self).to_representation(value)


class AncestorSerializer(ParentSerializer):
    children = serializers.PrimaryKeyRelatedField(many=True, required=False,
                            queryset=Ancestor.objects.all())
    siblings = serializers.PrimaryKeyRelatedField(many=True, required=False,
                            queryset=Ancestor.objects.all())
    parents = ParentsPrimaryKeyRelatedField(many=True,
                                            queryset=Ancestor.objects.all())

    class Meta:
        extra_kwargs = {'ancestors': {'read_only': True}}
        model = Ancestor
        fields = '__all__'

    def create(self, validated_data):
        siblings = validated_data.pop('siblings', [])
        parents = validated_data.pop('parents', [])
        is_owner = validated_data.pop('is_owner', False)
        if not parents:
            for sibling in siblings:
                for parent in sibling.parents.all():
                    parents.append(parent)
        if not parents:
            parents.append(Ancestor.objects.create(abstract=True))
        children = validated_data.pop('children', False)
        user = self.context.get('request').user
        if is_owner:
            validated_data['user'] = user
        ancestor = Ancestor.objects.create(**validated_data)
        if not is_owner:
            update_ancestors(user.ancestor.get().id, ancestor.id, 'create')
        # Children should have the same parents
        siblings.append(ancestor)
        if parents and siblings:
            for sibling in siblings:
                for parent in parents:
                    sibling.parents.add(parent)
        for child in children:
            child.parents.add(ancestor)
        return ancestor
