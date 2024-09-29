from django.urls import path
from .views.categories import CategoryView
from .views.products import ProductsView
from .views.product_details import ProductDetailsView
from .views.dietary_details import DietaryDetailView
from .views.unit import UnitView

urlpatterns = [
    path("categories/", CategoryView.as_view(), name="Categories"),
    path("products/", ProductsView.as_view(), name="Products"),
    path(
        "product/<int:product_id>/",
        ProductDetailsView.as_view(),
        name="Product Details",
    ),
    path(
        "dietary-details/",
        DietaryDetailView.as_view(),
        name="Dietary Details",
    ),
    path(
        "units/",
        UnitView.as_view(),
        name="Units",
    ),
]
