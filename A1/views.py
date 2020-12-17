from django.shortcuts import render , redirect
from django.forms import inlineformset_factory
from .models import (
    Product,
    Customer,
    Order,
)
from .forms import OrderForm , CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from .filters import Orderfilter
from django.contrib.auth.decorators import login_required







def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = Order.objects.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'customers': customers,
               'orders': orders,
               'delivered': delivered,
               'pending': pending,
               'total_orders': total_orders
               }
    return render(request, 'accounts/dashboard.html', context)

def Customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = Orderfilter(request.GET , queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer, 'orders': orders, 'order_count': order_count, 'myFilter':myFilter }
    return render(request,'accounts/customer.html', context)

def Prodects(request):
    products = Product.objects.all()

    return render(request,'accounts/products.html' , {'products': products})

def createOrder(request ,pk):
    OrderFormSet = inlineformset_factory(Customer , Order , fields=('product','status') , extra=2)
    customer = Customer.objects.get(id= pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance= customer)
    if request.method == 'POST':
        formset = OrderForm(request.POST,instance= customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context ={'formset' : formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST , instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'accounts/order_form.html',context)
def deleteOrder(request , pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request , 'accounts/delete.html',context)

def registerpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        context = {'form' : form}
        return render(request, 'accounts/register.html', context)


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password =  request.POST.get('password')
            user = authenticate(request , username = username , password = password)
            if user is not None:
                login(request , user)
                return redirect('home')
            else:
                messages.info(request , 'Username Or Password Not Correct')
        context = {}
        return render(request, 'accounts/login.html', context)

def logoutpage(request):
    logout(request)
    return redirect('login')
