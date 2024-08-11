from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category, Product


class ProductListView(ListView):
    model = Product
    template_name = "shop/list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            return Product.objects.filter(category=category, available=True)
        return Product.objects.filter(available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["category"] = (
            get_object_or_404(Category, slug=self.kwargs.get("category_slug"))
            if self.kwargs.get("category_slug")
            else None
        )
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/detail.html"
    context_object_name = "product"
