# Generated by Django 4.1 on 2025-03-26 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='book',
            new_name='book_id',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='order',
            new_name='order_id',
        ),
    ]
