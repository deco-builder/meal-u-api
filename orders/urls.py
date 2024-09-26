from django.urls import path
from .views.orders import OrderListView, OrderStatusUpdateView, OrderDetailView
from .views.checkout import CheckoutView
from .views.delivery_time_slot import DeliveryTimeSlotListView
from .views.delivery_location import DeliveryLocationListView
from .views.orders_warehouse import OrderWarehouseView
from .views.order_status import OrderStatusPreparingView, OrderStatusReadyToDeliverView

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/<int:order_id>/status/paid/", OrderStatusUpdateView.as_view(), name="order-status-paid"),
    path("<int:order_id>/status/preparing/", OrderStatusPreparingView.as_view(), name="order-status-preparing"),
    path("<int:order_id>/status/ready-to-deliver/", OrderStatusReadyToDeliverView.as_view(), name="order-status-ready-to-deliver"),
    path("orders/<int:order_id>/", OrderDetailView.as_view(), name="order-detail"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("delivery-time-slots/", DeliveryTimeSlotListView.as_view(), name="delivery-time-slots"),
    path("delivery-locations/", DeliveryLocationListView.as_view(), name="delivery-locations"),
    path("warehouse/", OrderWarehouseView.as_view(), name="order-warehouse"),
]
