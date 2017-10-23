from rest_framework import routers

from api.ancestors.views import AncestorViewSet
from api.photos.views import PhotoViewSet
from api.user.views import UserViewSet

router = routers.DefaultRouter()
urlpatterns = []
router.register(r'ancestors', AncestorViewSet)
router.register(r'users', UserViewSet)
router.register(r'photos', PhotoViewSet)

urlpatterns = []

urlpatterns += router.urls
