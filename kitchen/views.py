from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cook, Dish, DishType


@login_required
def index(request):
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }

    return render(request, "kitchen/index.html", context=context)

class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    queryset = DishType.objects.all()
    paginate_by = 5

   # def get_context_data(
   #     self, *, object_list=None, **kwargs
   # ):
   #     context = super(DishTypeListView, self).get_context_data(**kwargs)
   #     name = self.request.GET.get("name", "")
   #     context["search_form"] = DishTypeSearchForm(
   #         initial={"name": name}
   #     )
   #     return context

    #def get_queryset(self):
    #    form = DishTypeSearchForm(self.request.GET)
    #    if form.is_valid():
    #        return self.queryset.filter(
    #            name__icontains=form.cleaned_data["name"]
    #        )
    #    return self.queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5
    queryset = Dish.objects.select_related("dish_type")

   # def get_context_data(
   #     self, *, object_list=None, **kwargs
   # ):
   #     context = super(DishListView, self).get_context_data(**kwargs)
   #     name = self.request.GET.get("name", "")
   #     context["search_form"] = DishSearchForm(
   #         initial={"name": name}
   #     )
   #     return context

   # def get_queryset(self):
   #     form = DishSearchForm(self.request.GET)
   #     if form.is_valid():
   #         return self.queryset.filter(
   #             model__icontains=form.cleaned_data["name"]
   #         )
   #     return self.queryset

class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    queryset = Cook.objects.all()
    paginate_by = 5

 #   def get_context_data(
 #       self, *, object_list=None, **kwargs
 #   ):
 #       context = super(CookListView, self).get_context_data(**kwargs)
 #       username = self.request.GET.get("username", "")
 #       context["search_form"] = CookSearchForm(
 #           initial={"username": username}
 #       )
 #       return context

 #   def get_queryset(self):
 #       form = CookSearchForm(self.request.GET)
 #       if form.is_valid():
 #           return self.queryset.filter(
 #               username__icontains=form.cleaned_data["username"]
 #           )
 #       return self.queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("cooks__dish_type")
