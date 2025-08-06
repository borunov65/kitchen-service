from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from kitchen.models import Ingredient


INGREDIENT_URL = reverse("kitchen:ingredient-list")


class PublicIngredientTest(TestCase):
    def test_login_required(self):
        res = self.client.get(INGREDIENT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateIngredientTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_ingredients(self):
        Ingredient.objects.create(name="Milk")
        Ingredient.objects.create(name="Flour")
        response = self.client.get(INGREDIENT_URL)
        self.assertEqual(response.status_code, 200)
        dish_types = Ingredient.objects.all()
        self.assertEqual(
            list(response.context["ingredient_list"]),
            list(dish_types),
        )
        self.assertTemplateUsed(response, "kitchen/ingredient_list.html")

    def test_search_ingredient_by_name_returns_correct_results(self):
        Ingredient.objects.create(name="Milk")
        Ingredient.objects.create(name="Flour")
        response = self.client.get(INGREDIENT_URL, {"name": "mi"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Milk")
        self.assertNotContains(response, "Flour")

    def test_search_ingredient_by_name_no_match(self):
        Ingredient.objects.create(name="Milk")
        Ingredient.objects.create(name="Flour")
        response = self.client.get(INGREDIENT_URL, {"name": "Sugar"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Milk")
        self.assertNotContains(response, "Flour")
        self.assertEqual(
            list(response.context["ingredient_list"]),
            []
        )

    def test_search_dish_type_without_query_returns_all(self):
        Ingredient.objects.create(name="Milk")
        Ingredient.objects.create(name="Flour")
        response = self.client.get(INGREDIENT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Milk")
        self.assertContains(response, "Flour")
