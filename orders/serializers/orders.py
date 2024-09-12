from rest_framework import serializers
from ..models import Orders

class OrderSerializer(serializers.ModelSerializer):

    order_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Orders
        fields = '__all__'  

    def get_order_status(self, obj):
        return obj.order_status.name 