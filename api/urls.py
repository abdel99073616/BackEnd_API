from django.contrib import admin
from django.urls import path , include
from .views import(
    CustomerListAPIVeiw,
    CustomerCreateAPIVeiw,
    CustomerUpdateListAPIVeiw,
    CustomerRetieveAPIVeiw,
    CustomerDestroyAPIView,
)

urlpatterns = [
    path('Customer/' , CustomerListAPIVeiw.as_view() ) ,
    path('Customer/create' , CustomerCreateAPIVeiw.as_view() ) ,
    path('Customer/<pk>' , CustomerRetieveAPIVeiw.as_view() ) ,
    path('Customer/<pk>/edit' , CustomerUpdateListAPIVeiw.as_view() ) ,
    path('Customer/<pk>/delete' , CustomerDestroyAPIView.as_view() ) ,
]