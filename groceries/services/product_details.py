from django.db.models import Q
from ..models import Product
from ..serializers.product_details import ProductDetailsSerializer


class ProductDetailsService:
    def get(self, product_id):
        try:
            product = product = Product.objects.select_related("productnutrition").get(id=product_id)
            return ProductDetailsSerializer(product).data
        except Exception as e:
            raise e
