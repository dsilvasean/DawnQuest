from . import views
from rest_framework import routers
from django.urls import path,include

router = routers.DefaultRouter()
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),
    path('assessment/test', views.AssessmentTest.as_view(), name="test"),
]

        