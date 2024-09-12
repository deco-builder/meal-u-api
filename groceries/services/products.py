from django.db.models import Q
from ..models import Product
from ..serializers.products import ProductsSerializer


class ProductsService:
    def get(self, categories=None, dietary_details=None, search=None):
        try:
            queryset = Product.objects.select_related(
                "category_id", "unit_id"
            ).prefetch_related("productdietarydetail_set__dietary_details")

            if categories:
                queryset = queryset.filter(category_id__name__in=categories)

            if dietary_details:
                queryset = queryset.filter(
                    productdietarydetail__dietary_details__name__in=dietary_details
                ).distinct()

            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) | Q(description__icontains=search)
                )

            if dietary_details:
                queryset = queryset.filter(
                    productdietarydetail__dietary_details__name__in=dietary_details
                ).distinct()

            products = queryset.all()
            serializer = ProductsSerializer(products, many=True)
            return serializer.data
        except Exception as e:
            raise e