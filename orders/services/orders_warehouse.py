from collections import defaultdict
from ..models import DeliveryDetails
from ..serializers.orders import OrderSerializer


class OrderWarehouseService:
    def get(self):
        delivery_details = DeliveryDetails.objects.select_related("delivery_time", "order").all()
        grouped_orders = defaultdict(lambda: defaultdict(list))

        for detail in delivery_details:
            delivery_date = str(detail.delivery_date)
            time_slot = str(detail.delivery_time.start_time)
            grouped_orders[delivery_date][time_slot].append(detail.order)

        response_data = {}
        for date, times in grouped_orders.items():
            response_data[str(date)] = {}
            for time_slot, orders in times.items():
                response_data[str(date)][time_slot] = OrderSerializer(orders, many=True).data

        return response_data
