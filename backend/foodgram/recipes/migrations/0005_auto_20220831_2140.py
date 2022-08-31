# Generated by Django 2.2.19 on 2022-08-31 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20220831_2051'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amountingredient',
            options={'ordering': ('recipe',), 'verbose_name': 'Количество ингрединента', 'verbose_name_plural': 'Количества ингрединентов'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name',), 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('id',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('name',), 'verbose_name': 'Тэг', 'verbose_name_plural': 'Тэги'},
        ),
    ]
