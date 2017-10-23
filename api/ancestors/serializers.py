from django.conf import settings
from rest_framework import serializers

from ancestors.models import Ancestor
from ancestors.tasks import update_ancestors
from api.photos.serializers import PhotoSerializer
from api.user.serializers import UserSerializer
from my_ancestors.users.models import User


class ParentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=False,
                               queryset=User.objects.all())
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
    parents = ParentsPrimaryKeyRelatedField(many=True, required=False,
                                            queryset=Ancestor.objects.all())

    class Meta:
        extra_kwargs = {'ancestors': {'read_only': True},
                        'first_name': {'required': False},
                        'last_name': {'required': False},
                        'parents': {'required': False},
                        'birth': {'required': False}}
        model = Ancestor
        fields = '__all__'

    @staticmethod
    def has_abstract_parent(ancestor):
        for parent in ancestor.parents.all():
            if parent.abstract:
                return True
        return False

    @staticmethod
    def get_all_siblings(siblings):
        """
        Sometimes user can pass not all siblings. This method add missed ones
        """
        result = set()
        for sibling in siblings:
            result.update(siblings)
            for person in sibling.siblings:
                result.add(person)
        return result

    def create(self, validated_data):
        siblings = validated_data.pop('siblings', [])
        parents = validated_data.pop('parents', set())
        children = validated_data.pop('children', [])
        is_owner = self.context.get('request').data.get('is_owner', False)
        # Further we need to know does ancestor has abstract parent or not
        abstract_parent = False
        if not parents:
            parents.add(Ancestor.objects.create(abstract=True))
            abstract_parent = True
        # Ancestors and all his siblings should share the same parents
        if siblings:
            siblings = self.get_all_siblings(siblings)
            for sibling in siblings:
                for parent in sibling.parents.filter(abstract=False):
                    parents.add(parent)
            # if your siblings have not-abstract parents, your should
            # pop abstract parent from parents list
            if abstract_parent and len(parents) > 1:
                parents.pop()
            for sibling in siblings:
                sibling.parents.clear()
                for parent in parents:
                    sibling.parents.add(parent)

        user = self.context.get('request').user
        if is_owner:
            validated_data['user'] = user
        ancestor = Ancestor.objects.create(**validated_data)
        for parent in parents:
            ancestor.parents.add(parent)
        # Celery task "update_ancestors" used for adding new ancestor to filed
        # "ancestors" for all related ancestors
        if not is_owner:
            update_ancestors(user.ancestor.id, ancestor.id, 'create')
        for child in children:
            child.parents.add(ancestor)
            update_ancestors(ancestor, child, 'create')
        return ancestor


    def update(self, instance, validated_data):
        instance.birth = validated_data.get('birth', instance.birth)
        instance.death = validated_data.get('death', instance.death)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.user = validated_data.get('user', instance.user)
        siblings = validated_data.pop('siblings', [])
        parents = validated_data.pop('parents', [])
        children = validated_data.pop('children', [])
        is_owner = instance.user == self.context.get('request').user
        if parents:
            instance.parents.clear()
            for parent in parents:
                instance.parents.add(parent)

        for sibling in siblings:
            for parent in instance.parents.all():
                sibling.parents.add(parent)
        for child in children:
            child.parents.add(instance)
        instance.save()
        return instance



