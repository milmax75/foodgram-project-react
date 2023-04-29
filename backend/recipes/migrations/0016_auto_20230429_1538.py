# Generated by Django 2.2.19 on 2023-04-29 15:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_auto_20230429_0810'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredients',
            old_name='units',
            new_name='measurement_unit',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='cooktime',
            new_name='cooking_time',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='description',
            new_name='text',
        ),
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Add at least 1 ingredient')], verbose_name='количество'),
        ),
    ]