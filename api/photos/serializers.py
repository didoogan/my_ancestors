from rest_framework import serializers

from photos.models import Photo


class PhotoSerializer(serializers.ModelSerializer):

    photo = serializers.ImageField(required=False)
    photos = serializers.ListField(write_only=True,
        child=serializers.FileField(max_length=100000,
                                    allow_empty_file=False,
                                    use_url=False)
    )

    class Meta:
        model = Photo
        fields = ('id', 'photo', 'photos', 'uploaded', 'ancestor')

    def create(self, validated_data):
        photos = validated_data.pop('photos')
        for photo in photos:
            photo = Photo.objects.create(photo=photo, **validated_data)
        return photo
