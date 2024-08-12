import django_filters
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()
    brand = django_filters.CharFilter(field_name='brand', lookup_expr='icontains')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    rating = django_filters.NumberFilter(method='filter_by_rating')

    class Meta:
        model = Product
        fields = ['category', 'price', 'brand', 'rating']

    def filter_by_rating(self, queryset, name, value):
        return queryset.filter(rating__gte=value)
