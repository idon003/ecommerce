from django.urls import path
from .views import OrderListView, OrderDetailView, OrderHistoryView, OrderTrackingView


urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
    path('order-tracking/<int:order_id>/', OrderTrackingView.as_view(), name='order-tracking'),
]
