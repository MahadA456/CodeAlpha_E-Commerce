from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('update_cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:pk>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:pk>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
