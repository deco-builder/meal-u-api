from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name

class DietaryDetail(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT, null=False, blank=False)
    unit_id = models.ForeignKey(Unit, on_delete=models.PROTECT, null=False, blank=False)
    unit_size = models.DecimalField(decimal_places=2, max_digits=6, null=False, blank=False)
    price_per_unit = models.DecimalField(decimal_places=2, max_digits=6, null=False, blank=False)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class IngredientDietaryDetail(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    dietary_details = models.ForeignKey(DietaryDetail, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('ingredient', 'dietary_details')

class Nutrition(models.Model):
    ingredient_id = models.OneToOneField(Ingredient, primary_key=True, on_delete=models.CASCADE)
    carb = models.DecimalField(decimal_places=2, max_digits=6, null=False)
    protein = models.DecimalField(decimal_places=2, max_digits=6, null=False)
    fat = models.DecimalField(decimal_places=2, max_digits=6, null=False)
    calories = models.DecimalField(decimal_places=2, max_digits=6, null=False)