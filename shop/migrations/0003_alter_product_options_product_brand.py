# Generated by Django 4.2.5 on 2024-08-12 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_alter_product_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="product",
            name="brand",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
