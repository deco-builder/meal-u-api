from rest_framework import serializers
from ..models import Orders, DeliveryDetails
from .delivery_details import DeliveryDetailsSerializer 
from ..models import Orders, OrderProducts, OrderRecipes, OrderMealKits

class OrderSerializer(serializers.ModelSerializer):

    order_status = serializers.SerializerMethodField()
    delivery_details = serializers.SerializerMethodField()  # Add this to include delivery details
    item_names = serializers.SerializerMethodField()  # Custom field to combine names of products, recipes, and meal kits
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
    
    def get_item_names(self, obj):
        # This method extracts and combines names of products, recipes, and meal kits related to the order
        
        # Get product names
        product_names = obj.orderproducts_set.values_list('product__name', flat=True)
        
        # Get recipe names
        recipe_names = obj.orderrecipes_set.values_list('recipe__name', flat=True)
        
        # Get meal kit names
        mealkit_names = obj.ordermealkits_set.values_list('mealkit__name', flat=True)

        # Combine all the names into one list
        all_names = list(product_names) + list(recipe_names) + list(mealkit_names)
        return all_names