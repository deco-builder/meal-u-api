from django.urls import path
from .views.orders import OrderListView, OrderStatusPaidUpdateView, OrderDetailView, OrderStatusDeliveringUpdateView, OrderStatusDeliveredUpdateView, OrderStatusCompletedUpdateView
from .views.checkout import CheckoutView 
from .views.delivery_time_slot import DeliveryTimeSlotListView
from .views.delivery_location import DeliveryLocationListView
from .views.orders_warehouse import OrderWarehouseView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:order_id>/status/paid/', OrderStatusPaidUpdateView.as_view(), name='order-status-paid'),
    path('<int:order_id>/status/delivering/', OrderStatusDeliveringUpdateView.as_view(), name='order-status-delivering'),
    path('<int:order_id>/status/delivered/', OrderStatusDeliveredUpdateView.as_view(), name='order-status-delivered'),
    path('<int:order_id>/status/completed/', OrderStatusCompletedUpdateView.as_view(), name='order-status-delivered'),
    path('order-details/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('delivery-time-slots/', DeliveryTimeSlotListView.as_view(), name='delivery-time-slots'),
    path('delivery-locations/', DeliveryLocationListView.as_view(), name='delivery-locations'),
    path('warehouse/', OrderWarehouseView.as_view(), name='order-warehouse'),
]
