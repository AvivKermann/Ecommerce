# Generated by Django 4.2.5 on 2023-12-04 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0010_listing_watchlist_delete_watchlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="winning_bid",
            field=models.ImageField(
                blank=True, max_length=10000, null=True, upload_to=""
            ),
        ),
    ]
