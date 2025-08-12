from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cook, Dish, DishType, Ingredient
from .forms import (
    CookCreationForm,
    CookUpdateForm,
    DishForm,
    DishSearchForm,
    CookSearchForm,
    DishTypeSearchForm,
    IngredientForm,
    IngredientSearchForm
)


@login_required
def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()
    num_ingredients = Ingredient.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_ingredients": num_ingredients,
        "num_visits": num_visits + 1,
    }

    return render(request, "kitchen/index.html", context=context)


class PageBackgroundMixin:
    page_bg_url = None  # дефолтне значення, якщо не вказати у класі

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.page_bg_url:
            context["page_bg"] = self.page_bg_url
        return context


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    queryset = DishType.objects.all()
    paginate_by = 5

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(
            initial={"name": name}
        )
        context["page_bg"] = "https://images.pexels.com/photos/2403391/pexels-photo-2403391.jpeg"
        return context

    def get_queryset(self):
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return self.queryset


class DishTypeCreateView(LoginRequiredMixin, PageBackgroundMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"
    page_bg_url = "https://images.pexels.com/photos/8951247/pexels-photo-8951247.jpeg"


class DishTypeUpdateView(LoginRequiredMixin, PageBackgroundMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"
    page_bg_url = "https://images.pexels.com/photos/4252138/pexels-photo-4252138.jpeg"


class DishTypeDeleteView(LoginRequiredMixin, PageBackgroundMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_confirm_delete.html"
    page_bg_url = "https://images.pexels.com/photos/6937457/pexels-photo-6937457.jpeg"


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 2
    queryset = Dish.objects.select_related("dish_type")

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )
        context["page_bg"] = "https://images.pexels.com/photos/2403392/pexels-photo-2403392.jpeg"
        return context

    def get_queryset(self):
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return self.queryset


class DishDetailView(LoginRequiredMixin, PageBackgroundMixin, generic.DetailView):
    model = Dish
    page_bg_url = "https://images.pexels.com/photos/2403391/pexels-photo-2403391.jpeg"


class DishCreateView(LoginRequiredMixin, PageBackgroundMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")
    page_bg_url = "https://images.pexels.com/photos/8680488/pexels-photo-8680488.jpeg"


class DishUpdateView(LoginRequiredMixin, PageBackgroundMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")
    page_bg_url = "https://images.pexels.com/photos/18483758/pexels-photo-18483758.jpeg"


class DishDeleteView(LoginRequiredMixin, PageBackgroundMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")
    page_bg_url = "https://images.pexels.com/photos/19671307/pexels-photo-19671307.jpeg"


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    queryset = Cook.objects.all()
    paginate_by = 5

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(
            initial={"username": username}
        )
        context["page_bg"] = "https://images.pexels.com/photos/5251019/pexels-photo-5251019.jpeg"
        return context

    def get_queryset(self):
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


class CookDetailView(LoginRequiredMixin, PageBackgroundMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__dish_type")
    page_bg_url = "https://images.pexels.com/photos/32383604/pexels-photo-32383604.jpeg"


class CookCreateView(LoginRequiredMixin, PageBackgroundMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    page_bg_url = "https://images.pexels.com/photos/14786462/pexels-photo-14786462.jpeg"


class CookUpdateView(LoginRequiredMixin, PageBackgroundMixin, generic.UpdateView):
    model = Cook
    form_class = CookUpdateForm
    success_url = reverse_lazy("kitchen:cook-list")
    page_bg_url = "https://images.pexels.com/photos/7434505/pexels-photo-7434505.jpeg"
    template_name = "kitchen/cook_update_form.html"


class CookDeleteView(LoginRequiredMixin, PageBackgroundMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")
    page_bg_url = "https://images.pexels.com/photos/31769316/pexels-photo-31769316.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"


@login_required
def toggle_assign_to_dish(request, pk):
    cook = Cook.objects.get(id=request.user.id)
    if (
        Dish.objects.get(id=pk) in cook.dishes.all()
    ):  # probably could check if dish exists
        cook.dishes.remove(pk)
    else:
        cook.dishes.add(pk)
    return HttpResponseRedirect(reverse_lazy("kitchen:dish-detail", args=[pk]))


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    paginate_by = 5

    def get_context_data(
        self, *, object_list=None, **kwargs
    ):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = IngredientSearchForm(
            initial={"name": name}
        )
        context["page_bg"] = "https://images.pexels.com/photos/6971733/pexels-photo-6971733.jpeg"
        return context

    def get_queryset(self):
        form = IngredientSearchForm(self.request.GET)
        if form.is_valid():
            return self.model.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return self.model.objects.all()


class IngredientCreateView(LoginRequiredMixin, PageBackgroundMixin, generic.CreateView):
    model = Ingredient
    form_class = IngredientForm
    success_url = reverse_lazy("kitchen:ingredient-list")
    page_bg_url = "https://images.pexels.com/photos/8680484/pexels-photo-8680484.jpeg"


class IngredientUpdateView(LoginRequiredMixin, PageBackgroundMixin, generic.UpdateView):
    model = Ingredient
    form_class = IngredientForm
    success_url = reverse_lazy("kitchen:ingredient-list")
    page_bg_url = "https://images.pexels.com/photos/28297954/pexels-photo-28297954.jpeg"


class IngredientDeleteView(LoginRequiredMixin, PageBackgroundMixin, generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")
    page_bg_url = "https://images.pexels.com/photos/1267320/pexels-photo-1267320.jpeg"
