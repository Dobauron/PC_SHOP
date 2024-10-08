from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Category, Product
from django_filters.views import FilterView
from .filters import ProductFilter
from django.db.models import Max


class ProductListView(FilterView):
    model = Product
    template_name = "shop/list.html"
    context_object_name = "products"
    paginate_by = 10
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset().filter(available=True)
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category, available=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["category"] = (
            get_object_or_404(Category, slug=self.kwargs.get("category_slug"))
            if self.kwargs.get("category_slug")
            else None
        )
        max_price = Product.objects.aggregate(max_price=Max("price"))["max_price"]
        context["max_price"] = max_price
        context["brands"] = Product.objects.values_list("brand", flat=True).distinct()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/detail.html"
    context_object_name = "product"
