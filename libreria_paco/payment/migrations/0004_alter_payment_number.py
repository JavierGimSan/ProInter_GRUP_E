# Generated by Django 5.1.7 on 2025-05-07 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_payment_cvc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='number',
            field=models.CharField(primary_key=True, serialize=False),
        ),
    ]
