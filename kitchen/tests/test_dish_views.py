from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from kitchen.models import Dish, DishType


DISH_URL = reverse("kitchen:dish-list")


class PublicDishTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_dishes(self):
        dish_type = DishType.objects.create(name="TestDishType")
        Dish.objects.create(name="Harcho", dish_type=dish_type, price=12.00)
        Dish.objects.create(name="Karbonara", dish_type=dish_type, price=15.50)
        response = self.client.get(DISH_URL)
        self.assertEqual(response.status_code, 200)
        dishes = Dish.objects.all()
        self.assertEqual(
            list(response.context["dish_list"]),
            list(dishes),
        )
        self.assertTemplateUsed(response, "kitchen/dish_list.html")

    def test_search_dishes_by_name_returns_correct_results(self):
        dish_type = DishType.objects.create(name="TestDishType")
        Dish.objects.create(name="Harcho", dish_type=dish_type, price=12.00)
        Dish.objects.create(name="Karbonara", dish_type=dish_type, price=15.50)
        response = self.client.get(DISH_URL, {"name": "ha"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harcho")
        self.assertNotContains(response, "Karbonara")

    def test_search_dish_by_name_no_match(self):
        dish_type = DishType.objects.create(name="TestDishType")
        Dish.objects.create(name="Harcho", dish_type=dish_type, price=12.00)
        Dish.objects.create(name="Karbonara", dish_type=dish_type, price=15.50)
        response = self.client.get(DISH_URL, {"name": "Varenyky"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Harcho")
        self.assertNotContains(response, "Karbonara")
        self.assertEqual(
            list(response.context["dish_list"]),
            []
        )

    def test_search_dish_without_query_returns_all(self):
        dish_type = DishType.objects.create(name="TestDishType")
        Dish.objects.create(name="Harcho", dish_type=dish_type, price=12.00)
        Dish.objects.create(name="Karbonara", dish_type=dish_type, price=15.50)
        response = self.client.get(DISH_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harcho")
        self.assertContains(response, "Karbonara")
