# Generated by Django 3.0.5 on 2020-05-12 12:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specialists', '0013_auto_20200511_1934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='criteria',
            name='id',
        ),
        migrations.AlterField(
            model_name='criteria',
            name='criteria_name',
            field=models.CharField(db_index=True, max_length=50, primary_key=True, serialize=False, verbose_name='Имя критерия'),
        ),
        migrations.AlterField(
            model_name='criteria',
            name='criteria_value',
            field=models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='Вес критерия'),
        ),
        migrations.CreateModel(
            name='Estim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=50, verbose_name='Имя критерия')),
                ('value', models.CharField(choices=[('0', 0), ('0.25', 0.25), ('0.5', 0.5), ('0.75', 0.75), ('1.0', 1.0)], max_length=10, verbose_name='Уровень владения')),
                ('criteria', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='specialists.Criteria')),
            ],
        ),
    ]
