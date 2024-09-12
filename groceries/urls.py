from django.urls import path
from .views.categories import CategoryView
from .views.products import ProductsView
from .views.product_details import ProductDetailsView

urlpatterns = [
    path("categories/", CategoryView.as_view(), name="Categories"),
    path("products/", ProductsView.as_view(), name="Products"),
    path(
        "product/<int:product_id>/",
        ProductDetailsView.as_view(),
        name="Product Details",
    ),
]
