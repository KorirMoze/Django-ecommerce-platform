from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)

    def __str__(self): 
        return self.name

class Category(models.Model):
    slug = models.SlugField(max_length=200,null=True,blank=False)
    name = models.CharField(max_length=200,null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2 )
    descriptions = models.TextField(max_length=500,null=True,blank=False)
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True, blank=True)
    trending = models.BooleanField(default=False,help_text="0=default, 1=Trending") 
    meta_title = models.CharField(max_length=200,null=False,blank=False)
    meta_keyword = models.CharField(max_length=200,null=False,blank=False)  
    status = models.BooleanField(default=False,help_text="0=default, 1=Hidden") 

    
    def __str__(self):
        return self.name   

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url  

class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True,null=True)
    slug = models.SlugField(max_length=200,null=True,blank=False)
    name = models.CharField(max_length=200,null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2 )
    old_price =  models.DecimalField(max_digits=7,decimal_places=2,null=True,)
    small_descriptions = models.CharField(max_length=500,null=True,blank=False)
    descriptions = models.TextField(max_length=500,null=True,blank=False)
    digital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null=True, blank=True)
    trending = models.BooleanField(default=False,help_text="0=default, 1=Trending")
    tag =  models.CharField(max_length=200,null=True,blank=False)
    status = models.BooleanField(default=False,help_text="0=default, 1=Hidden")
    def __str__(self):
        return self.name


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class ProductImage(models.Model):
    products = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.product.name



class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping=False
        ordereditems = self.ordereditem_set.all()
        for i in ordereditems:
            if i.product.digital == False:
                shipping = True
        return shipping


    @property
    def get_cart_total(self):
        ordereditems = self.ordereditem_set.all()
        total = sum([item.get_total for item in ordereditems])
        return total

    @property
    def get_cart_items(self):
        ordereditems = self.ordereditem_set.all()
        total = sum([item.quantity for item in ordereditems])
        return total

class orderedItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price*self.quantity
        return total

class Shipping(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zip_code = models.CharField(max_length=200,null=True)
    date_shipped = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

