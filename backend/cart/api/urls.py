from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    # path('cart/checkout/', views.CheckoutView.as_view(), name='checkout'),
]
