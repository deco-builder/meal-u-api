from django.db import models
from user_auth.models import User
from groceries.models import Product
from community.models import Recipe, MealKit
from django.core.validators import RegexValidator


class OrderStatuses(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name


class Orders(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_status = models.ForeignKey(OrderStatuses, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    passcode = models.CharField(
        max_length=4,
        validators=[RegexValidator(regex=r"^\d{4}$", message="Passcode must be a 4-digit numeric string.")],
        null=True,
        blank=True,
        help_text="A 4-digit numeric passcode for the order.",
    )
    total = models.DecimalField(decimal_places=2, max_digits=10)
    delivery_proof_photo = models.ImageField(upload_to='delivery_proofs/', null=True, blank=True)


class OrderProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("order", "product")

    quantity = models.PositiveIntegerField(null=False, blank=False)
    total = models.DecimalField(decimal_places=2, max_digits=10)


class OrderRecipes(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("order", "recipe")

    quantity = models.PositiveIntegerField(null=False, blank=False)
    total = models.DecimalField(decimal_places=2, max_digits=10)


class OrderMealKits(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    mealkit = models.ForeignKey(MealKit, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("order", "mealkit")

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
    delivery_fee = models.DecimalField(decimal_places=2, max_digits=10)
    longitude = models.DecimalField(decimal_places=4, null=True, max_digits=8)
    latitude = models.DecimalField(decimal_places=4, null=True, max_digits=8)


    def __str__(self):
        return self.name + " " + self.branch


class DeliveryTimeSlot(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    cut_off = models.TimeField(null=False, blank=False)

    def __str__(self):
        return self.name + " " + str(self.start_time) + " - " + str(self.end_time)


class DeliveryStatus(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)


class Lockers(models.Model):
    location = models.ForeignKey(DeliveryLocation, on_delete=models.CASCADE, null=False, blank=False)
    locker_number = models.CharField(
        max_length=10, null=False, blank=False, unique=True, help_text="Unique locker number for this location"
    )
    is_occupied = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Locker {self.locker_number} at {self.location}"


class DeliveryDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=False, blank=False)
    delivery_location = models.ForeignKey(DeliveryLocation, on_delete=models.PROTECT, null=False, blank=False)
    delivery_time = models.ForeignKey(DeliveryTimeSlot, on_delete=models.PROTECT, null=False, blank=False)
    delivery_date = models.DateField()
    locker = models.ForeignKey(Lockers, on_delete=models.SET_NULL, null=True, blank=True)
    qr_code = models.TextField(
        null=True,
        blank=True,
        help_text="String combination of delivery location, delivery time, delivery date, and order.",
    )

    def __str__(self):
        return f"Delivery {self.order} at {self.delivery_location} on {self.delivery_date}"

    def save(self, *args, **kwargs):
        if self.locker:
            self.qr_code = f"{self.delivery_location.name}_{self.delivery_time.name}_{self.delivery_date}_{self.order.id}_{self.locker.locker_number}"
        else:
            self.qr_code = None
        super(DeliveryDetails, self).save(*args, **kwargs)


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
    payment_method = models.ForeignKey("users.UserPaymentMethod", on_delete=models.PROTECT, null=False, blank=False)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.PROTECT, null=False, blank=False)
    amount = models.DecimalField(decimal_places=2, max_digits=3)
    payment_date = models.DateTimeField()
    transaction_id = models.CharField(max_length=255)
