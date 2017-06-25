from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ancestors.models import Ancestor
from api.ancestors.serializers import AncestorSerializer


class AncestorViewSet(viewsets.ModelViewSet):
    queryset = Ancestor.objects.all()
    serializer_class = AncestorSerializer
    permission_classes = (IsAuthenticated,)
