from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.photos.serializers import PhotoSerializer
from photos.models import Photo

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
