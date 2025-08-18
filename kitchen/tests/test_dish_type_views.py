from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from kitchen.models import DishType


DISH_TYPE_URL = reverse("kitchen:dish-type-list")


class PublicDishTypeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_TYPE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTypeTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_types(self):
        DishType.objects.create(name="Cakes")
        DishType.objects.create(name="Pasta")
        response = self.client.get(DISH_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        dish_types = DishType.objects.all()
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dish_types),
        )
        self.assertTemplateUsed(response, "kitchen/dish_type_list.html")

    def test_search_dish_tipe_by_name_returns_correct_results(self):
        DishType.objects.create(name="Cakes")
        DishType.objects.create(name="Pasta")
        response = self.client.get(DISH_TYPE_URL, {"name": "ca"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cakes")
        self.assertNotContains(response, "Pasta")

    def test_search_dish_type_by_name_no_match(self):
        DishType.objects.create(name="Cakes")
        DishType.objects.create(name="Pasta")
        response = self.client.get(DISH_TYPE_URL, {"name": "Pizza"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Cakes")
        self.assertNotContains(response, "Pasta")
        self.assertEqual(
            list(response.context["dish_type_list"]),
            []
        )

    def test_search_dish_type_without_query_returns_all(self):
        DishType.objects.create(name="Cakes")
        DishType.objects.create(name="Pasta")
        response = self.client.get(DISH_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cakes")
        self.assertContains(response, "Pasta")
