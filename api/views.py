from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView ,
    RetrieveAPIView ,
    UpdateAPIView ,
    DestroyAPIView ,
    CreateAPIView ,
)
from A1.models import(
    Customer,
    Order,
    Product
)

from .serializers import(
    CustomerSerializer,
    OrderSerializer,
    ProductSerializer
)

########### Customer ###############

class CustomerListAPIVeiw(ListAPIView):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer

class CustomerCreateAPIVeiw(CreateAPIView):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer

class CustomerUpdateListAPIVeiw(UpdateAPIView):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer

class CustomerRetieveAPIVeiw(RetrieveAPIView):
    queryset=Customer.objects.all()
    serializer_class=CustomerSerializer

class CustomerDestroyAPIView(DestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
