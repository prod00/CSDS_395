# Generated by Django 3.2.12 on 2022-02-25 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applicase', '0005_alter_student_case_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tapositionpost',
            name='title',
        ),
    ]
