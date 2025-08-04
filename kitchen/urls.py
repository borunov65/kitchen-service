from django.urls import path

from .models import DishType
from .views import (
    index,
    DishListView,
    DishDetailView,
 #   CarUpdateView,
    CookListView,
    CookDetailView,
 #   DriverCreateView,
 #   DriverLicenseUpdateView,
 #   DriverDeleteView,
    DishTypeListView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
  #  toggle_assign_to_car,
)


urlpatterns = [
    path("", index, name="index"),

    path(
        "dish_types/",
        DishTypeListView.as_view(),
        name="dish-type-list",
    ),
    path(
        "dish_types/create/",
        DishTypeCreateView.as_view(),
        name="dish-type-create",
    ),
    path(
        "dish_types/<int:pk>/update/",
        DishTypeUpdateView.as_view(),
        name="dish-type-update",
    ),
    path(
        "dish_types/<int:pk>/delete/",
        DishTypeDeleteView.as_view(),
        name="dish-type-delete",
    ),
    path("dishs/", DishListView.as_view(), name="dish-list"),
    path("dishs/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path(
        "cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"
    ),
]

app_name = "kitchen"
