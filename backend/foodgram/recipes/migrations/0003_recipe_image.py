# Generated by Django 2.2.19 on 2022-08-30 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220830_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=1, upload_to='recipe_images/', verbose_name='Изображение блюда'),
            preserve_default=False,
        ),
    ]
