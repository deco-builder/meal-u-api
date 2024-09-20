# Generated by Django 5.1 on 2024-09-18 09:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("community", "0002_initial"),
        ("groceries", "0001_initial"),
        ("orders", "0001_initial"),
        ("users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="deliveries",
            name="courier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="deliveries",
            name="delivery_details",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="orders.deliverydetails"
            ),
        ),
        migrations.AddField(
            model_name="deliverydetails",
            name="delivery_location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="orders.deliverylocation",
            ),
        ),
        migrations.AddField(
            model_name="deliveries",
            name="delivery_status",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="orders.deliverystatus"
            ),
        ),
        migrations.AddField(
            model_name="deliverydetails",
            name="delivery_time",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="orders.deliverytimeslot",
            ),
        ),
        migrations.AddField(
            model_name="lockers",
            name="courier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="lockers",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="orders.deliverylocation",
            ),
        ),
        migrations.AddField(
            model_name="ordermealkits",
            name="mealkit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="community.mealkit"
            ),
        ),
        migrations.AddField(
            model_name="orderpayment",
            name="payment_method",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="users.userpaymentmethod",
            ),
        ),
        migrations.AddField(
            model_name="orderproducts",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="groceries.product"
            ),
        ),
        migrations.AddField(
            model_name="orderrecipes",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="community.recipe"
            ),
        ),
        migrations.AddField(
            model_name="orders",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="orderrecipes",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="orders.orders"
            ),
        ),
        migrations.AddField(
            model_name="orderproducts",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="orders.orders"
            ),
        ),
        migrations.AddField(
            model_name="orderpayment",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="orders.orders"
            ),
        ),
        migrations.AddField(
            model_name="ordermealkits",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="orders.orders"
            ),
        ),
        migrations.AddField(
            model_name="deliverydetails",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="orders.orders"
            ),
        ),
        migrations.AddField(
            model_name="deliveries",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="orders.orders"
            ),
        ),
        migrations.AddField(
            model_name="orders",
            name="order_status",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="orders.orderstatuses"
            ),
        ),
        migrations.AddField(
            model_name="orderpayment",
            name="payment_status",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="orders.paymentstatus"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="orderrecipes",
            unique_together={("order", "recipe")},
        ),
        migrations.AlterUniqueTogether(
            name="orderproducts",
            unique_together={("order", "product")},
        ),
        migrations.AlterUniqueTogether(
            name="ordermealkits",
            unique_together={("order", "mealkit")},
        ),
    ]
