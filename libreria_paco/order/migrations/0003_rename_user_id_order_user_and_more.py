# Generated by Django 4.1 on 2025-03-26 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_rename_user_order_user_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='book_id',
            new_name='book',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='order_id',
            new_name='order',
        ),
    ]
