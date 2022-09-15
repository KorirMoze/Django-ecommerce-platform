from calendar import c
from multiprocessing import context
from urllib import request

from django.shortcuts import render,redirect
from .models import*
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart,cartData,guestOrder
from django.contrib import messages

# Create your views here.
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

    customer = request.user.customer
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


def PView(request, cat_slug, pro_slug):
    if(Category.objects.filter(slug=cat_slug, status=0)):
        if(Product.objects.filter(slug=pro_slug,status=0)):
            products=Product.objects.filter(slug=pro_slug,status=0).first()
            context={'products':products}
        else:
            messages.error(request,'no such product')
            return redirect('collection')
    else:
        messages.error(request,'no such category')
        return redirect('collection')
    return render(request,'store/pView.html',context)
   


    


    
