from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from ancestors.models import Ancestor
from api.ancestors.serializers import AncestorSerializer


class AncestorViewSet(viewsets.ModelViewSet):
    queryset = Ancestor.objects.all()
    serializer_class = AncestorSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        ids_str = request.query_params.get('ids', False)
        if ids_str:
            ids = ids_str.split(',')
            queryset =  Ancestor.objects.filter(id__in=ids)
        else:
            queryset = Ancestor.objects.all()
        if request.query_params.get('without_user', False):
            queryset = queryset.filter(user__isnull=True)
        serializer = AncestorSerializer(queryset, many=True)
        return Response(serializer.data)
