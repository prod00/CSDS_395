# Generated by Django 3.2.12 on 2022-04-17 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicase', '0006_tapositionchat'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='application',
        ),
        migrations.AddField(
            model_name='message',
            name='position',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='applicase.tapositionpost'),
            preserve_default=False,
        ),
    ]
