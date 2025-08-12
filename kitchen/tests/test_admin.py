from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin"
        )
        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="cook",
            password="testcook",
        )

    def test_cook_years_of_experience_listed(self):
        """
        Test thet cook's years of experience is in list_display
        on cook admin page
        :return:
        """
        url = reverse("admin:kitchen_cook_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.cook.years_of_experience)

    def test_cook_detail_years_of_experience_listed(self):
        """
        Test thet cook's years of experience is on cook detail admin page
        :return:
        """
        url = reverse("admin:kitchen_cook_change", args=[self.cook.id])
        res = self.client.get(url)
        self.assertContains(res, self.cook.years_of_experience)

    def test_cook_add_years_of_experience_listed(self):
        """
        Tst thet cook's years_of_experience is present in the add form
        in the admin page
        :return:
        """
        url = reverse("admin:kitchen_cook_add")
        res = self.client.get(url)
        self.assertContains(res, "years_of_experience")
