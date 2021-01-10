from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('shop/', views.shop, name="shop"),
    path('gallery/', views.gallery, name="gallery"),
    path('team/', views.team, name="team"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('shop/<str:name>', views.productView, name="product"),
    path('update_item/', views.updateItem, name="update_item"),
    path('remove_item/', views.removeItem, name="remove_item"),
    path('process_order/', views.processOrder, name="process_order")
]
