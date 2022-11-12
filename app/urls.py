from django.urls import path
from .views import RegisterViewSet, UpdateUserViewSet, UpdateVehicleViewSet, AdsViewSet

urlpatterns = [
    path("register/", RegisterViewSet.as_view({"post": "create"}), name="user-create"),
    path(
        "update/<int:pk>/",
        UpdateUserViewSet.as_view({"put": "update"}),
        name="user-update",
    ),
    path(
        "vehicle/<int:pk>/",
        UpdateVehicleViewSet.as_view({"put": "update"}),
        name="vehicle-update",
    ),
    path("ads/", AdsViewSet.as_view(), name="ads-create"),
    path("ads/<int:pk>/", AdsViewSet.as_view(), name="ads-update"),
    path("ads/<int:pk>/", AdsViewSet.as_view(), name="ads-delete"),
]
