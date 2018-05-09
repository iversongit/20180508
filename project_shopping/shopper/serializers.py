from rest_framework import serializers
from shopper.models import Goods

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ['productid','productname','price','marketprice']

    def to_representation(self, instance): # 将实例序列化
        data = super().to_representation(instance) # 获取每个商品的信息
        try:
            data['productlongname'] = instance.productlongname
        except Exception as e:
            data['productlongname'] = ""
        return data