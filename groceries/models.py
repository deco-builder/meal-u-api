from django.db import models
from user_auth.models import User

class Categories(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.name

class DietaryDetails(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.name

class Units(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name

class Ingredients(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    category_id = models.ForeignKey(Categories, on_delete=models.PROTECT, null=False, blank=False)
    unit_id = models.ForeignKey(Units, on_delete=models.PROTECT, null=False, blank=False)
    unit_size = models.DecimalField(decimal_places=2, max_digits=3, null=False, blank=False)
    price_per_unit = models.DecimalField(decimal_places=2, max_digits=3, null=False, blank=False)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class IngredientDietaryDetails(models.Model):
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    dietary_details = models.ForeignKey(DietaryDetails, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('ingredient', 'dietary_details')

class Nutrition(models.Model):
    ingredient_id = models.OneToOneField(Ingredients, primary_key=True, on_delete=models.CASCADE)
    carb = models.DecimalField(decimal_places=2, max_digits=3, null=False)
    protein = models.DecimalField(decimal_places=2, max_digits=3, null=False)
    fat = models.DecimalField(decimal_places=2, max_digits=3, null=False)
    calories = models.DecimalField(decimal_places=2, max_digits=3, null=False)