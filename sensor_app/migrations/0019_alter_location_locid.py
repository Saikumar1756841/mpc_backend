# Generated by Django 4.1.1 on 2025-05-30 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sensor_app", "0018_alter_location_locid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="locId",
            field=models.CharField(
                default="LOC19588", editable=False, max_length=50, unique=True
            ),
        ),
    ]
