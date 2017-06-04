from django.http import JsonResponse
from rest_framework import viewsets

from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerizlizer


class UserViewSet(viewsets.ModelViewSet):
    # renderer_classes = (JsonResponse, )
    queryset = get_user_model().objects.all()
    serializer_class = UserSerizlizer
    permission_classes = (IsAuthenticated,)


def get_csrf(request):
    return JsonResponse()
