from calendar import c
from gc import get_objects
from multiprocessing import context
from urllib import request

from django.shortcuts import render,redirect,get_object_or_404
from .models import*
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart,cartData,guestOrder
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import createUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticatedUser,allowed_users
# Create your views here.

@unauthenticatedUser
def register(request):
 
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
           
            messages.success(request,'Account was created ' + user)
            return redirect('login')

    context = {'form':form}
    return render(request,'store/register.html',context)

def custome(request):
    current_user = request.user

@unauthenticatedUser
def loginpage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
     
        if user is not None:
            login(request, user)
            return redirect('store')
    context = {}
    return render(request,'store/login.html',context)

def logoutpage(request):
    logout(request)
    return redirect('store')

def store(request,):

        data = cartData(request)
        cartItems = data['cartItems']
        category = Category.objects.filter(status=0)
        products = Product.objects.all()
        context = {'products':products,'cartItems':cartItems,'category':category,}
        return render(request,'store/collection.html',context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order =data['order']
    items = data['items']
   

    context = {'items':items,'order':order,'cartItems':cartItems}
    return render (request, 'store/cart.html',context)

def checkout(request):

     data = cartData(request)
     cartItems = data['cartItems']
     order =data['order']
     items = data['items']

     context = {'items':items,'order':order, 'cartItems':cartItems}
     return render (request, 'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:', action)
    print('productId:', productId)
    user = request.user
    customer,created = Customer.objects.get_or_create(
        email=user.email,
        username = user.username,

            
        )
    customer.name = user.username
    customer.save()
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem,created = orderedItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
       orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was Added',safe=False)
#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)


    else:
       customer,order = guestOrder(request, data)

    total = float( data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
            order.complete = True
    order.save()

    if order.shipping == True:
        Shipping.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zip_code=data['shipping']['zipcode'],
            )
            

    return JsonResponse('payment completed',safe=False) 


def Collection(request):
    data = cartData(request)
    category = Category.objects.filter(status=0)
    products = Product.objects.all()
    cartItems = data['cartItems']
    context={'category':category,'products':products,'cartItems':cartItems}
    return render(request,'store/collection.html', context)
    

def collectionView(request,slug):
    data = cartData(request)
    if(Category.objects.filter(slug=slug,status=0)):
        products = Product.objects.filter(category__slug = slug)
        cartItems = data['cartItems']
        category = Category.objects.filter(slug=slug).first()
        context = {'products':products,'category':category,'cartItems':cartItems}
        return render(request,'store/trial.html',context)
    else:
        messages.warning(request, 'no such category')
        return redirect('collections')

def productView(request, cate_slug, prod_slug):
    if(Category.objects.filter(slug=cate_slug, status=0)):
        if(Product.objects.filter(slug=prod_slug,status=0)):
            products=Product.objects.filter(slug=prod_slug,status=0).first()
            context={'products':products}
        else:
            messages.error(request,'no such product')
            return redirect('collection')
    else:
        messages.error(request,'no such category')
        return redirect('collection')
    return render(request,'store/productview.html',context)


def PView(request, id, slug):
    category = Category.objects.all()
   #products = Product.objects.filter(slug=pro_slug,status=0)
    product=Product.objects.get(pk=id) 
    context={'product':product,'category':category}
     
    return render(request,'store/pView.html',context)

def view(request, pk, *args, **kwargs ):
    #product = Product.objects.get(id=pk)
    product = get_object_or_404(Product,id=pk)
    context = {'product':product}

    return render(request,'store/pView.html',context)
   
def UserProfile(request,pk):
    user = User.objects.get(id=pk)
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'user':user,'cartItems':cartItems}
    return render(request,'store/profile.html',context)


def updateUser(request):
    context = {}
    return render(request,'store/update_profile.html')


    
