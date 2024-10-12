# Generated by Django 5.1.1 on 2024-10-12 03:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category/')),
            ],
        ),
        migrations.CreateModel(
            name='DietaryDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('unit_size', models.DecimalField(decimal_places=2, help_text='Size of the product', max_digits=6)),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=6)),
                ('measurement_size', models.DecimalField(decimal_places=2, help_text='Size of the measurement unit (e.g., 100 for 100g)', max_digits=6, null=True)),
                ('price_per_measurement', models.DecimalField(blank=True, decimal_places=2, help_text='Price for the given measurement size', max_digits=6)),
                ('description', models.TextField()),
                ('stock', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='groceries.category')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PreparationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('additional_price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groceries.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductNutrition',
            fields=[
                ('product_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='groceries.product')),
                ('servings_per_package', models.PositiveIntegerField(null=True)),
                ('serving_size', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('energy_per_serving', models.DecimalField(decimal_places=2, help_text='in kJ', max_digits=6, null=True)),
                ('protein_per_serving', models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True)),
                ('fat_total_per_serving', models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True)),
                ('saturated_fat_per_serving', models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True)),
                ('carbohydrate_per_serving', models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True)),
                ('sugars_per_serving', models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True)),
                ('dietary_fibre_per_serving', models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True)),
                ('sodium_per_serving', models.DecimalField(decimal_places=2, help_text='in mg', max_digits=6, null=True)),
                ('energy_per_100g', models.DecimalField(decimal_places=2, help_text='in kJ', max_digits=6, null=True)),
                ('protein_per_100g', models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True)),
                ('fat_total_per_100g', models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True)),
                ('saturated_fat_per_100g', models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True)),
                ('carbohydrate_per_100g', models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True)),
                ('sugars_per_100g', models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True)),
                ('dietary_fibre_per_100g', models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True)),
                ('sodium_per_100g', models.DecimalField(decimal_places=2, help_text='in mg', max_digits=6, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='unit_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='groceries.unit'),
        ),
        migrations.CreateModel(
            name='ProductDietaryDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dietary_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groceries.dietarydetail')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groceries.product')),
            ],
            options={
                'unique_together': {('product', 'dietary_details')},
            },
        ),
    ]
