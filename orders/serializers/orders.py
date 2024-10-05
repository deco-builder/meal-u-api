from rest_framework import serializers
from ..models import Orders, DeliveryDetails
from ..models import Orders
from ..models import DeliveryDetails, DeliveryLocation, DeliveryTimeSlot
from user_auth.models import User
from rest_framework import serializers

class DeliveryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLocation
        fields = ['name', 'branch', 'address_line1', 'address_line2', 'city', 'postal_code', 'country', 'details']

class DeliveryTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryTimeSlot
        fields = ['name', 'start_time', 'end_time', 'cut_off']

class DeliveryDetailsSerializer(serializers.ModelSerializer):
    delivery_location = DeliveryLocationSerializer()
    delivery_time = DeliveryTimeSlotSerializer()

    class Meta:
        model = DeliveryDetails
        fields = ['delivery_location', 'delivery_time', 'delivery_date']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'image'] 

class OrderSerializer(serializers.ModelSerializer):

    order_status = serializers.SerializerMethodField()
    delivery_details = serializers.SerializerMethodField()  # Add this to include delivery details
    item_names = serializers.SerializerMethodField()  # Custom field to combine names of products, recipes, and meal kits
    user_id = UserSerializer(read_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'order_status', 'delivery_details', 'item_names', 'created_at', 'updated_at', 'total', 'delivery_proof_photo', 'user_id']  

    def get_order_status(self, obj):
        return obj.order_status.name 
    
    def get_delivery_details(self, obj):
        # Assuming each order has one delivery detail, otherwise modify this
        delivery_detail = DeliveryDetails.objects.filter(order=obj).first()
        if delivery_detail:
            return DeliveryDetailsSerializer(delivery_detail).data
        else:
            print(f"No delivery details found for order {obj.id}")
        return None
    
    def get_item_names(self, obj):
        # This method extracts and combines names of products, recipes, and meal kits related to the order
        
         # Get product names and quantities
        product_items = obj.orderproducts_set.values('product__name', 'quantity')
        product_list = [{'name': item['product__name'], 'quantity': item['quantity']} for item in product_items]
        
        # Get recipe names and quantities
        recipe_items = obj.orderrecipes_set.values('recipe__name', 'quantity')
        recipe_list = [{'name': item['recipe__name'], 'quantity': item['quantity']} for item in recipe_items]
        
        # Get meal kit names and quantities
        mealkit_items = obj.ordermealkits_set.values('mealkit__name', 'quantity')
        mealkit_list = [{'name': item['mealkit__name'], 'quantity': item['quantity']} for item in mealkit_items]

        # Combine all the items into one list
        all_items = product_list + recipe_list + mealkit_list
        return all_items