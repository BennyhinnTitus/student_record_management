from rest_framework import routers
from .views import StudentViewSet

router = routers.DefaultRouter()
router.register(r'', StudentViewSet)   # creates routes automatically

urlpatterns = router.urls
