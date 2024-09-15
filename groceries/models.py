from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to="category/", blank=True, null=True)

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

class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT, null=False, blank=False)
    unit_id = models.ForeignKey(Unit, on_delete=models.PROTECT, null=False, blank=False)
    unit_size = models.DecimalField(decimal_places=2, max_digits=6, null=False, blank=False, help_text="Size of the product")
    price_per_unit = models.DecimalField(decimal_places=2, max_digits=6, null=False, blank=False)
    measurement_size = models.DecimalField(decimal_places=2, max_digits=6, null=True, help_text="Size of the measurement unit (e.g., 100 for 100g)")
    price_per_measurement = models.DecimalField(decimal_places=2, max_digits=6, blank=True, help_text="Price for the given measurement size")
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    

    def calculate_price_per_measurement(self):
        if self.unit_size <= 0 or self.measurement_size <= 0:
            return None
        
        return (self.price_per_unit / self.unit_size) * self.measurement_size

    def save(self, *args, **kwargs):
        self.price_per_measurement = self.calculate_price_per_measurement()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductDietaryDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    dietary_details = models.ForeignKey(DietaryDetail, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'dietary_details')

class ProductNutrition(models.Model):
    product_id = models.OneToOneField(Product, primary_key=True, on_delete=models.CASCADE)
    servings_per_package = models.PositiveIntegerField(null=True)
    serving_size = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    energy_per_serving = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in kJ")
    protein_per_serving = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in grams")
    fat_total_per_serving = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in grams")
    saturated_fat_per_serving = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in grams")
    carbohydrate_per_serving = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in grams")
    sugars_per_serving = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in grams")
    dietary_fibre_per_serving = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in grams")
    sodium_per_serving = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in mg")
    
    energy_per_100g = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in kJ")
    protein_per_100g = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in grams")
    fat_total_per_100g = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in grams")
    saturated_fat_per_100g = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in grams")
    carbohydrate_per_100g = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in grams")
    sugars_per_100g = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in grams")
    dietary_fibre_per_100g = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in grams")
    sodium_per_100g = models.DecimalField(max_digits=6, decimal_places=2, null=True, help_text="in mg")
