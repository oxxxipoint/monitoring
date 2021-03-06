# Generated by Django 3.0.5 on 2020-05-11 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specialists', '0012_specialist_main_estim'),
    ]

    operations = [
        migrations.CreateModel(
            name='Criteria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criteria_name', models.CharField(db_index=True, max_length=50, verbose_name='Имя критерия')),
                ('criteria_value', models.DecimalField(decimal_places=1, max_digits=2, verbose_name='Вес критерия')),
            ],
            options={
                'verbose_name': 'Критерий',
                'verbose_name_plural': 'Критерии',
            },
        ),
        migrations.AlterField(
            model_name='dictobj',
            name='key',
            field=models.CharField(db_index=True, max_length=50, verbose_name='Имя критерия'),
        ),
        migrations.AlterField(
            model_name='dictobj',
            name='value',
            field=models.CharField(choices=[('0', 0), ('0.25', 0.25), ('0.5', 0.5), ('0.75', 0.75), ('1.0', 1.0)], max_length=10, verbose_name='Уровень владения'),
        ),
    ]
