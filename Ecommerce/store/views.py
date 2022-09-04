from django.shortcuts import render
from .models import*
from django.http import JsonResponse
# Create your views here.

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render (request, 'store/store.html',context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items= order.ordereditem_set.all()
    else:
        items=[]
        order = {'order.get_cart_items':0,'order.get_cart_total':0}
    context = {'items':items,'order':order}
    return render (request, 'store/cart.html',context)

def checkout(request):
  
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items= order.ordereditem_set.all()
    else:
        items=[]
        order = {'order.get_cart_items':0,'order.get_cart_total':0}
    context = {'items':items,'order':order}
    return render (request, 'store/checkout.html',context)

def updateItem(request):
    return JsonResponse('Item was Added',safe=False)