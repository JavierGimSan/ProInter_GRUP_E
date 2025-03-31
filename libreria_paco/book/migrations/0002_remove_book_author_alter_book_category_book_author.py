# Generated by Django 4.1 on 2025-03-31 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(related_name='categories', to='book.category'),
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(related_name='authors', to='book.author'),
        ),
    ]
