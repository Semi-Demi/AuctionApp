# Generated by Django 4.1 on 2024-11-13 01:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0005_auctionitem_delete_auction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auctionitem",
            name="itemId",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]