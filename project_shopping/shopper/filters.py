import django_filters
from rest_framework import filters
from shopper.models import Goods

class GoodsFilter(filters.FilterSet):
    class Meta:
        model = Goods
        fields = ['productid','productname','price','marketprice']
