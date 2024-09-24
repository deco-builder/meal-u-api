from rest_framework import serializers
from ..models import Orders, DeliveryDetails
from .delivery_details import DeliveryDetailsSerializer 

class OrderSerializer(serializers.ModelSerializer):

    order_status = serializers.SerializerMethodField()
    delivery_details = serializers.SerializerMethodField()  # Add this to include delivery details
    
    class Meta:
        model = Orders
        fields = '__all__'  

    def get_order_status(self, obj):
        return obj.order_status.name 
    
    def get_delivery_details(self, obj):
        # Assuming each order has one delivery detail, otherwise modify this
        delivery_detail = DeliveryDetails.objects.filter(order=obj).first()
        if delivery_detail:
            # Debugging: Print out delivery details fetched
            print(f"Delivery details for order {obj.id}: {delivery_detail}")
            return DeliveryDetailsSerializer(delivery_detail).data
        else:
            print(f"No delivery details found for order {obj.id}")
        return None