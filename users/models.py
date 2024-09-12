# from django.db import models
# from user_auth.models import User
# from orders.models import DeliveryLocation, PaymentMethod

# class AccountStatus(models.Model):
#     name = models.CharField(max_length=255, null=False, blank=False)

#     def __str__(self):
#         return self.name

# class Roles(models.Model):
#     name = models.CharField(max_length=255, null=False, blank=False)

#     def __str__(self):
#         return self.name

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     role = models.ForeignKey(Roles, on_delete=models.PROTECT)
#     status = models.ForeignKey(AccountStatus, on_delete=models.PROTECT)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     profile_pic = models.URLField()
#     phone_number = models.CharField(max_length=20)

# class UserPaymentMethod(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
#     token = models.CharField(max_length=255, unique=True, null=False)
#     last_four_digits = models.CharField(max_length=4, null=False)
#     expiration_date = models.DateField(null=False)

# class UserDeliveryLocation(models.Model):
#     user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
#     delivery_location = models.ForeignKey(DeliveryLocation, null=False, blank=False, on_delete=models.CASCADE)
#     is_default = models.BooleanField()
