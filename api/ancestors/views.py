from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ancestors.models import Ancestor
from api.ancestors.serializers import AncestorSerializer


class AncestorViewSet(viewsets.ModelViewSet):
    queryset = Ancestor.objects.all()
    serializer_class = AncestorSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        return Response({'message': 'Not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
