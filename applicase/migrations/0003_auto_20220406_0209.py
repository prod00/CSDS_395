# Generated by Django 3.2.12 on 2022-04-06 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicase', '0002_departments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departments',
            name='id',
        ),
        migrations.AlterField(
            model_name='departments',
            name='department',
            field=models.CharField(max_length=45, primary_key=True, serialize=False),
        ),
    ]