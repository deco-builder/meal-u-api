from collections import defaultdict
from ..models import DeliveryDetails
from ..serializers.orders import OrderSerializer
from datetime import datetime
from django.utils.timezone import make_aware


class OrderWarehouseService:
    def get(self, start_date=None, end_date=None):
        now = make_aware(datetime.now())
        
        delivery_details = DeliveryDetails.objects.select_related("delivery_time", "order") \
            .filter(delivery_date__gte=now.date())

        if start_date:
            delivery_details = delivery_details.filter(delivery_date__gte=start_date)
        if end_date:
            delivery_details = delivery_details.filter(delivery_date__lte=end_date)

        delivery_details = delivery_details.order_by("delivery_date", "delivery_time__start_time")

        grouped_orders = defaultdict(lambda: defaultdict(list))

        for detail in delivery_details:
            delivery_date = str(detail.delivery_date)
            time_slot = str(detail.delivery_time.start_time)
            grouped_orders[delivery_date][time_slot].append(detail.order)

        response_data = {}
        for date, times in grouped_orders.items():
            response_data[date] = {}
            for time_slot, orders in times.items():
                response_data[date][time_slot] = OrderSerializer(orders, many=True).data

        return response_data
