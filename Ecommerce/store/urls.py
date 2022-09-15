from django.urls import path

from .import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('collection/', views.Collection, name="collection"),
	path('collectionsView/<str:slug>/', views.collectionView,name="collectionsView"),
	path('productView/<str:cate_slug>/<str:prod_slug>/',views.productView,name="productView"),
	path('pView/<str:cat_slug>/<pro_slug>/', views.PView, name="pView"),
]