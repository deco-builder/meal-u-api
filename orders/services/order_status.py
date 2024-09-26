from ..models import OrderStatuses, Orders, Lockers, DeliveryDetails
import random
from django.db.models import Q
from .orders import OrdersService


class OrderStatusPreparingService:
    def post(self, order_id):
        try:
            try:
                PAID_STATUS = OrderStatuses.objects.get(name="paid")
            except Exception as e:
                raise e
            
            order = Orders.objects.get(id=order_id)
            if order.order_status != PAID_STATUS:
                raise Exception(f"Order with id {order_id} as invalid current status to update into preparing")
            
            try:
                PREPARING_STATUS = OrderStatuses.objects.get(name="preparing")
            except Exception as e:
                raise e
            
            order.order_status = PREPARING_STATUS
            passcode = self.generate_unique_passcode()
            order.passcode = passcode
            order.save()

            delivery_details = DeliveryDetails.objects.get(order=order_id)
            delivery_details.locker = self.find_empty_locker(
                delivery_details.delivery_location, delivery_details.delivery_date, delivery_details.delivery_time
            )
            delivery_details.save()

            return OrdersService.get_order_details(order_id)

        except Orders.DoesNotExist:
            raise Exception(f"Order with id {order_id} does not exist")
        except Exception as e:
            raise e

    def generate_unique_passcode(self):
        completed_status = OrderStatuses.objects.filter(name__iexact="completed").first()

        if completed_status:
            existing_passcodes = set(
                Orders.objects.filter(~Q(order_status=completed_status)).values_list("passcode", flat=True)
            )
        else:
            existing_passcodes = set(Orders.objects.all().values_list("passcode", flat=True))

        while True:
            passcode = f"{random.randint(0, 9999):04d}"
            if passcode not in existing_passcodes:
                return passcode

    def find_empty_locker(self, delivery_location, delivery_date, delivery_time):
        all_lockers = Lockers.objects.filter(location=delivery_location)

        occupied_lockers = DeliveryDetails.objects.filter(
            delivery_location=delivery_location,
            delivery_date=delivery_date,
            delivery_time=delivery_time,
            locker__isnull=False,
        ).values_list("locker", flat=True)

        empty_locker = all_lockers.exclude(id__in=occupied_lockers).filter(is_occupied=False).first()

        return empty_locker


class OrderStatusReadyToDeliverService:
    def post(self, order_id):
        try:
            try:
                PREPARING_STATUS = OrderStatuses.objects.get(name="preparing")
            except Exception as e:
                raise e
            
            order = Orders.objects.get(id=order_id)
            if order.order_status != PREPARING_STATUS:
                raise Exception(f"Order with id {order_id} has invalid current status to update into ready to deliver")

            try:
                READY_TO_DELIVER_STATUS = OrderStatuses.objects.get(name="ready to deliver")
            except Exception as e:
                raise e
            
            order.order_status = READY_TO_DELIVER_STATUS
            order.save()
            return OrdersService.get_order_details(order_id)
        except Orders.DoesNotExist:
            raise Exception(f"Order with id {order_id} does not exist")
        except Exception as e:
            raise e
