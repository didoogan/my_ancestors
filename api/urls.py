from django.conf.urls import url, include
from rest_framework import routers

from api.ancestors.views import AncestorViewSet
from api.user.views import UserViewSet

router = routers.DefaultRouter()
urlpatterns = []
router.register(r'ancestors', AncestorViewSet)
router.register(r'users', UserViewSet)

urlpatterns = []

urlpatterns += router.urls
