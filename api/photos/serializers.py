from rest_framework import serializers

from photos.models import Photo


class PhotoSerializer(serializers.ModelSerizlizer):
    class Meta:
        model = Photo
        fields = '__all__'
