from django.shortcuts import render , redirect
from django.forms import inlineformset_factory
from .models import (
    Product,
    Customer,
    Order,
)
from .forms import OrderForm , CreateUserForm ,CustomerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import Group
from django.contrib import messages
from .filters import Orderfilter
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user , allowed_users , admin_only

@login_required(login_url='login')
@admin_only
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = Orderfilter(request.GET , queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer, 'orders': orders, 'order_count': order_count, 'myFilter':myFilter }
    return render(request,'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Prodects(request):
    products = Product.objects.all()

    return render(request,'accounts/products.html' , {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request ,pk):
    OrderFormSet = inlineformset_factory(Customer , Order , fields=('product','status') , extra=2)
    customer = Customer.objects.get(id= pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance= customer)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context ={'formset' : formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request , pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('home')
    context = {'item':order}
    return render(request , 'accounts/delete.html',context)

@unauthenticated_user
def registerpage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    context = {'form' : form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginpage(request):
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders ,
               'total_orders':total_orders ,
               'delivered' :delivered ,
               'pending':pending,
               }
    return render(request, 'accounts/user.html' , context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
    customer= request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST , request.FILES , instance=customer)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request , 'accounts/account_settings.html' , context)
