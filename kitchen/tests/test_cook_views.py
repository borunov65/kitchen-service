from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from kitchen.models import Cook


COOK_URL = reverse("kitchen:cook-list")


class PublicCookTest(TestCase):
    def test_login_required(self):
        res = self.client.get(COOK_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCookTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_cooks(self):
        Cook.objects.create(
            username="test_username1"
        )
        Cook.objects.create(
            username="test_username2"
        )
        response = self.client.get(COOK_URL)
        self.assertEqual(response.status_code, 200)
        cooks = Cook.objects.all()
        self.assertEqual(
            list(response.context["cook_list"]),
            list(cooks),
        )
        self.assertTemplateUsed(response, "kitchen/cook_list.html")

    def test_search_cook_by_username_returns_correct_results(self):
        Cook.objects.create(
            username="test_username"
        )
        Cook.objects.create(
            username="otheruser"
        )
        response = self.client.get(COOK_URL, {"username": "test_username"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_username")
        self.assertNotContains(response, "otheruser")

    def test_search_cook_by_username_no_match(self):
        Cook.objects.create(
            username="test_username"
        )
        Cook.objects.create(
            username="otheruser"
        )
        response = self.client.get(COOK_URL, {"username": "anotheuther"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "test_username")
        self.assertNotContains(response, "otheruser")
        self.assertEqual(
            list(response.context["cook_list"]),
            []
        )

    def test_search_cook_without_query_returns_all(self):
        Cook.objects.create(
            username="test_username"
        )
        Cook.objects.create(
            username="otheruser"
        )
        response = self.client.get(COOK_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_username")
        self.assertContains(response, "otheruser")

    def test_create_cook(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "years_of_experience": 8,
        }
        self.client.post(reverse("kitchen:cook-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.years_of_experience, form_data["years_of_experience"])
