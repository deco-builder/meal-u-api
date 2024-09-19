# Generated by Django 5.1 on 2024-09-18 09:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cart", "0001_initial"),
        ("community", "0001_initial"),
        ("groceries", "0001_initial"),
        ("user_auth", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserCart",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name="cartingredient",
            name="recipe_ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="community.recipeingredient",
            ),
        ),
        migrations.AddField(
            model_name="cartmealkit",
            name="mealkit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="community.mealkit"
            ),
        ),
        migrations.AddField(
            model_name="cartproduct",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="groceries.product"
            ),
        ),
        migrations.AddField(
            model_name="cartrecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="community.recipe"
            ),
        ),
        migrations.AddField(
            model_name="cartrecipe",
            name="user_cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart_recipes",
                to="cart.usercart",
            ),
        ),
        migrations.AddField(
            model_name="cartproduct",
            name="user_cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart_products",
                to="cart.usercart",
            ),
        ),
        migrations.AddField(
            model_name="cartmealkit",
            name="user_cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart_mealkits",
                to="cart.usercart",
            ),
        ),
        migrations.AddField(
            model_name="cartingredient",
            name="user_cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart_ingredients",
                to="cart.usercart",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="cartrecipe",
            unique_together={("user_cart", "recipe")},
        ),
        migrations.AlterUniqueTogether(
            name="cartproduct",
            unique_together={("user_cart", "product")},
        ),
        migrations.AlterUniqueTogether(
            name="cartmealkit",
            unique_together={("user_cart", "mealkit")},
        ),
        migrations.AlterUniqueTogether(
            name="cartingredient",
            unique_together={("user_cart", "recipe_ingredient")},
        ),
    ]
