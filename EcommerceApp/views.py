from django.contrib.auth.models import Group

from django.shortcuts import render, redirect
from .models import Customer, Product, Orders
from .forms import OrderForm, ProductForm, CustomerForm, CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from .decorator import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    product = Product.objects.all()
    orders = Orders.objects.all()

    total_orders = len(orders)
    pending_orders = orders.filter(status='Pending').count()
    delivered_orders = orders.filter(status='Delivered').count()
    outfordelivery_orders = orders.filter(status='Outfordelivery').count()

    context = {'customers': customers,
               'product': product,
               'orders': orders,
               'total_orders': total_orders,
               'pending_orders': pending_orders,
               'delivered_orders': delivered_orders,
               'outfordelivery_orders': outfordelivery_orders,
               }
    return render(request, 'accounts/dash.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Customers'])
def products(request):
    product = Product.objects.all()
    context = {'products': product}
    return render(request, 'accounts/product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Customers'])
def order(request):
    return render(request, 'accounts/order.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def update_order(request, pk):
    orders = Orders.objects.get(id=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=orders)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = OrderForm(instance=orders)
        context = {'form': form}
        return render(request, 'accounts/update_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin', 'Customers'])
def delete_order(request, pk):
    orders = Orders.objects.get(id=pk)
    orders.delete()
    return redirect('/')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def customer(request, pk):
    customers = Customer.objects.get(id=pk)
    orders = customers.orders_set.all()

    total_orders = len(orders)
    pending_orders = orders.filter(status='Pending').count()
    delivered_orders = orders.filter(status='Delivered').count()
    outfordelivery_orders = orders.filter(status='Outfordelivery').count()

    context = {'customers': customers,
               'orders': orders,
               'total_orders': total_orders,
               'pending_orders': pending_orders,
               'delivered_orders': delivered_orders,
               'outfordelivery_orders': outfordelivery_orders,
               }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products/')
    else:
        form = ProductForm()
        context = {'form': form}
        return render(request, 'accounts/add_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/products/')
    else:
        form = ProductForm(instance=product)
        context = {'form': form}
        return render(request, 'accounts/update_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('/products/')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = OrderForm()
        context = {'form': form}
        return render(request, 'accounts/add_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customers'])
def place_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = OrderForm()
        context = {'form': form}
        return render(request, 'accounts/add_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def update_customer(request, pk):
    customers = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customers)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customers)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        context = {'form': form}
        return render(request, 'accounts/update_customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_customer(request, pk):
    customers = Customer.objects.get(id=pk)
    customers.delete()
    return redirect('/')


@unauthenticated_user
def registerpage(request):
    form = CreateUserForm()
    context = {'form': form}
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = request.POST.get('username')
            group = Group.objects.get(name='Customers')
            user.groups.add(group)
            Customer.objects.create(
                user=user
            )
            messages.success(request, 'Account created successfully for'+ username)
            return redirect('login')
        else:
            messages.warning(request, 'Fill All The Fields.')
            return redirect('register')
    else:
        return render(request, 'accounts/registerpage.html', context)


@unauthenticated_user
def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Username or Password is Wrong.')
    return render(request, 'accounts/loginpage.html')


def logoutpage(request):
    logout(request)
    return redirect('login')


@allowed_users(allowed_roles=['Customers'])
def userpage(request):
    orders = request.user.customer.orders_set.all()

    total_orders = len(orders)
    pending_orders = orders.filter(status='Pending').count()
    delivered_orders = orders.filter(status='Delivered').count()
    outfordelivery_orders = orders.filter(status='Outfordelivery').count()

    context = {
               'orders': orders,
               'total_orders': total_orders,
               'pending_orders': pending_orders,
               'delivered_orders': delivered_orders,
               'outfordelivery_orders': outfordelivery_orders,
               }

    return render(request, 'accounts/userpage.html', context)


def account_settings(request):
    return render(request, 'accounts/account_setiings.html')
