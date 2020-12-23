from django.db import models
from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from A1.models import (
    Customer,
    Product,
    Order,
)



class CustomerSerializer(ModelSerializer):
    class Meta :
        model = Customer
        fields = '__all__'



class ProductSerializer(ModelSerializer):
    class Meta :
        model = Product
        fields = '__all__'



class OrderSerializer(ModelSerializer):
    class Meta :
        model = Order
        fields = '__all__'


