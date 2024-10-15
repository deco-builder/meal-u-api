from ..models import Category
from ..serializers.categories import CategorySerializer


class CategoryServices:
    def get(self):
        try:
            categories = Category.objects.order_by("name").all()
            serializer = CategorySerializer(categories, many=True)
            return serializer.data
        except Exception as e:
            raise e
