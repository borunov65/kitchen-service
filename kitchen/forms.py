from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from kitchen.models import Dish, Cook, DishType, Ingredient


class DishForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Dish
        fields = "__all__"


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by dish name"
            }
        )
    )


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
            "username",
            "email",
        )


class CookUpdateForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = [
            "first_name",
            "last_name",
            "years_of_experience",
            "username", "email"
        ]


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username"
            }
        )
    )


class DishTypeCreationForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = ("name",)


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by dish type name"
            }
        )
    )


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name"]
        widgets = {
            "dishes": forms.CheckboxSelectMultiple()
        }


class IngredientCreationForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ("name",)


class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by ingredients name"
            }
        )
    )
