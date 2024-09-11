# Generated by Django 5.1 on 2024-09-11 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceries', '0004_alter_nutrition_calories_alter_nutrition_carb_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nutrition',
            name='calories',
        ),
        migrations.RemoveField(
            model_name='nutrition',
            name='carb',
        ),
        migrations.RemoveField(
            model_name='nutrition',
            name='fat',
        ),
        migrations.RemoveField(
            model_name='nutrition',
            name='protein',
        ),
        migrations.AddField(
            model_name='nutrition',
            name='carbohydrate_per_100g',
            field=models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='carbohydrate_per_serving',
            field=models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='dietary_fibre_per_100g',
            field=models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='dietary_fibre_per_serving',
            field=models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='energy_per_100g',
            field=models.DecimalField(decimal_places=2, help_text='in kJ', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='energy_per_serving',
            field=models.DecimalField(decimal_places=2, help_text='in kJ', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='fat_total_per_100g',
            field=models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='fat_total_per_serving',
            field=models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='protein_per_100g',
            field=models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='protein_per_serving',
            field=models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='saturated_fat_per_100g',
            field=models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='saturated_fat_per_serving',
            field=models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='serving_size',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='servings_per_package',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='sodium_per_100g',
            field=models.DecimalField(decimal_places=2, help_text='in mg', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='sodium_per_serving',
            field=models.DecimalField(decimal_places=2, help_text='in mg', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='sugars_per_100g',
            field=models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='nutrition',
            name='sugars_per_serving',
            field=models.DecimalField(decimal_places=2, help_text='in grams', max_digits=6, null=True),
        ),
    ]
