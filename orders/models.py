from django.db import models
from user_auth.models import User
from groceries.models import Product
from community.models import Recipe, MealKit

class UserCart(models.Model):
    user_id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

class UserCartProducts(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_cart', 'product')

    quantity = models.PositiveIntegerField(default=0)

class UserCartRecipes(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_cart', 'recipe')

    quantity = models.PositiveIntegerField(default=0)

class UserCartMealKits(models.Model):
    user_cart = models.ForeignKey(UserCart, on_delete=models.CASCADE)
    mealkit = models.ForeignKey(MealKit, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_cart', 'mealkit')

    quantity = models.PositiveIntegerField(default=0)

class OrderStatuses(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

class Orders(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders" )
    order_status = models.ForeignKey(OrderStatuses, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    total = models.DecimalField(decimal_places=2, max_digits=10)

class OrderProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('order', 'product')

    quantity = models.PositiveIntegerField(null=False, blank=False)
    total = models.DecimalField(decimal_places=2, max_digits=10)

class OrderRecipes(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('order', 'recipe')

    quantity = models.PositiveIntegerField(null=False, blank=False)
    total = models.DecimalField(decimal_places=2, max_digits=10)

class OrderMealKits(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    mealkit = models.ForeignKey(MealKit, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('order', 'mealkit')

    quantity = models.PositiveIntegerField(null=False, blank=False)
    total = models.DecimalField(decimal_places=2, max_digits=10)

class DeliveryLocation(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    branch = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255, null=False, blank=False)
    address_line2 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    details = models.TextField()

class DeliveryTimeSlot(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    cut_off = models.TimeField(null=False, blank=False)

class DeliveryStatus(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

class DeliveryDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=False, blank=False)
    delivery_location = models.ForeignKey(DeliveryLocation, on_delete=models.PROTECT, null=False, blank=False)
    delivery_time = models.ForeignKey(DeliveryTimeSlot, on_delete=models.PROTECT, null=False, blank=False)
    delivery_date = models.DateField()

class Deliveries(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=False, blank=False)
    delivery_details = models.ForeignKey(DeliveryDetails, on_delete=models.PROTECT, null=False, blank=False)
    delivery_status = models.ForeignKey(DeliveryStatus, on_delete=models.PROTECT, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    courier = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)

class PaymentMethod(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

class PaymentStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

class OrderPayment(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=False, blank=False)
    payment_method = models.ForeignKey('users.UserPaymentMethod', on_delete=models.PROTECT, null=False, blank=False)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.PROTECT, null=False, blank=False)
    amount = models.DecimalField(decimal_places=2, max_digits=3)
    payment_date = models.DateTimeField()
    transaction_id = models.CharField(max_length=255)

class Lockers(models.Model):
    location = models.ForeignKey(DeliveryLocation, on_delete=models.CASCADE, null=False, blank=False)
    qr_code = models.TextField()
    passcode = models.CharField(max_length=10)
    is_occupied = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    courier = models.ForeignKey(User, on_delete=models.PROTECT)