# Generated by Django 5.1 on 2024-09-15 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0010_mealkit_created_at_mealkit_is_customized_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='photo',
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='recipes/'),
        ),
    ]
