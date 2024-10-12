from ..models import Product, PreparationType
from ..serializers.preparation_type import CategoryPreparationTypeSerializer


class ProductPreparationTypeService:
    def get(self, product_id):
        try:
            product = Product.objects.get(id=product_id)
            preparation_type = PreparationType.objects.filter(category=product.category_id).all().distinct()
            return CategoryPreparationTypeSerializer(preparation_type, many=True).data
        except Exception as e:
            raise e
