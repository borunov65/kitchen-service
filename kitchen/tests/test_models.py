from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import DishType, Dish, Ingredient


class ModelsTests(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(
            name="test"
        )
        self.assertEqual(
            str(dish_type),
            f"{dish_type.name}"
        )

    def test_cook_str(self):
        cook = get_user_model().objects.create(
            username="test",
            password="test123",
            first_name="test_first",
            last_name="test_last"
        )
        self.assertEqual(
            str(cook),
            f"{cook.username} ({cook.first_name} {cook.last_name})"
        )

    def test_dish_str(self):
        dish_type = DishType.objects.create(
            name="test"
        )
        dish = Dish.objects.create(
            name="Test",
            dish_type=dish_type,
            price=10.50
        )
        self.assertEqual(str(dish), dish.name)


    def test_ingredient_str(self):
        ingredient = Ingredient.objects.create(
            name="test"
        )
        self.assertEqual(
            str(ingredient),
            f"{ingredient.name}"
        )