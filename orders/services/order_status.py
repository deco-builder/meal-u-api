from ..models import OrderStatuses, Orders, Lockers, DeliveryDetails, OrderRecipes, OrderMealKits
from community.models import Recipe, MealKit
import random
from django.db.models import Q
from .orders import OrdersService
from PIL import Image
import io
from django.core.files.base import ContentFile

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

class OrderStatusPaidService:
    def post(self, order_id):
        try:
            try:
                PENDING_STATUS = OrderStatuses.objects.get(name="pending")
            except Exception as e:
                raise e
            
            order = Orders.objects.get(id=order_id)
            if order.order_status != PENDING_STATUS:
                raise Exception(f"Order with id {order_id} has invalid current status to update into paid")
            
            try:
                PAID_STATUS = OrderStatuses.objects.get(name="paid")
            except Exception as e:
                raise e
            
            order.order_status = PAID_STATUS
            order.save()

            total_revenue = 0
            for order_recipe in OrderRecipes.objects.filter(order=order):
                recipe = order_recipe.recipe
                if recipe.monetize:
                    author_cut = self.calculate_author_cut(recipe, order_recipe.quantity)
                    recipe.creator.voucher_credits += author_cut
                    total_revenue += author_cut
                    recipe.creator.save()

            for order_mealkit in OrderMealKits.objects.filter(order=order):
                mealkit = order_mealkit.mealkit
                if mealkit.monetize:
                    author_cut = self.calculate_author_cut(mealkit, order_mealkit.quantity)
                    mealkit.creator.voucher_credits += author_cut
                    total_revenue += author_cut
                    mealkit.creator.save()
            
        except Orders.DoesNotExist:
            raise Exception(f"Order with id {order_id} does not exist")
        except Exception as e:
            raise e

    def calculate_author_cut(self, item, quantity):
        if isinstance(item, Recipe):
            return item.price * quantity * 0.1  
        elif isinstance(item, MealKit):
            return item.price * quantity * 0.1  
        return 0
        
class OrderStatusDeliveringService:
    def post(self, order_id):
        try:
            try:
                READY_TO_DELIVER_STATUS = OrderStatuses.objects.get(name="ready to deliver")
            except Exception as e:
                raise e
            
            order = Orders.objects.get(id=order_id)
            if order.order_status != READY_TO_DELIVER_STATUS:
                raise Exception(f"Order with id {order_id} has invalid current status to update into delivering")
            
            try:
                DELIVERING_STATUS = OrderStatuses.objects.get(name="delivering")
            except Exception as e:
                raise e
            
            order.order_status = DELIVERING_STATUS
            order.save()
        except Orders.DoesNotExist:
            raise Exception(f"Order with id {order_id} does not exist")
        except Exception as e:
            raise e

class OrderStatusDeliveredService:
    def post(self, order_id, photo_proof):
        try:
            try:
                DELIVERING_STATUS = OrderStatuses.objects.get(name="delivering")
            except Exception as e:
                raise e
            
            order = Orders.objects.get(id=order_id)
            if order.order_status != DELIVERING_STATUS:
                raise Exception(f"Order with id {order_id} has invalid current status to update into delivered")
            
            try:
                DELIVERED_STATUS = OrderStatuses.objects.get(name="delivered")
            except Exception as e:
                raise e
            if not photo_proof:
                raise Exception("Photo proof is required to mark the order as 'delivered'.")
            
            image = Image.open(photo_proof)
            image = image.convert("RGB") 

            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=70)  
            compressed_image = ContentFile(buffer.getvalue(), name=photo_proof.name)

            order.delivery_proof_photo.save(photo_proof.name, compressed_image, save=True)
            order.order_status = DELIVERED_STATUS
            order.save()
        except Orders.DoesNotExist:
            raise Exception(f"Order with id {order_id} does not exist")
        except Exception as e:
            raise e

class OrderStatusCompletedService:
    def post(self, order_id, user_passcode):
        try:
            try:
                DELIVERED_STATUS = OrderStatuses.objects.get(name="delivered")
            except Exception as e:
                raise e
            
            order = Orders.objects.get(id=order_id)
            if order.order_status != DELIVERED_STATUS:
                raise Exception(f"Order with id {order_id} has invalid current status to update into completed")
            
            try:
                COMPLETED_STATUS = OrderStatuses.objects.get(name="completed")
            except Exception as e:
                raise e
            if order.passcode != user_passcode:
                raise Exception("Invalid passcode")       
            
            order.order_status = COMPLETED_STATUS
            order.save()
        except Orders.DoesNotExist:
            raise Exception(f"Order with id {order_id} does not exist")
        except Exception as e:
            raise e

