from django.urls import path

from .import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('collection/', views.Collection, name="collection"),
	path('collectionsView/<str:slug>/', views.collectionView,name="collectionsView"),
	path('productView/<str:cate_slug>/<str:prod_slug>/',views.productView,name="productView"),
	path('pView/<int:id><str:slug>/', views.PView, name="pView"),
	path('view/<str:pk>/', views.view, name="view"),
	path('login/',views.loginpage, name="login"),
	path('register/',views.register, name="register"),
	path('logou/',views.logout, name="logout"),

]