# Generated by Django 3.1.7 on 2021-03-26 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20210326_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='product_variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imgs', to='products.productvariant'),
        ),
    ]