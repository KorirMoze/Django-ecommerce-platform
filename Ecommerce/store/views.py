from calendar import c
from email import message
from multiprocessing import context
from nis import cat
from unicodedata import category
from django.shortcuts import render
from .models import*
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart,cartData,guestOrder
from django.contrib import messages

# Create your views here.

def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
 

    products = Product.objects.all()

    context = {'products':products,'cartItems':cartItems}
    return render (request, 'store/store.html',context)

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
    category = Category.objects.filter(status=0)
    context={'category':category}
    return render(request,'store/collection.html', context)

def collectionView(request,slug):
    if(Category.objects.filter(slug=slug,status=0)):
        product = Product.objects.filter(category__slug = slug)
        category_name = category.objects.filter(slug=slug).first()
        context = {'product':product,'category_name':category_name}
        return render(request,'store/store.html',context)
    else:
        messages.warning(request, 'no such category')

def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
 

    products = Product.objects.all()

    context = {'products':products,'cartItems':cartItems}
    