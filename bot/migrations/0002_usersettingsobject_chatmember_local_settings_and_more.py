# Generated by Django 5.0.8 on 2024-09-30 13:04

import django.db.models.deletion
import uuid
from django.db import migrations, models


def populate_new_field(apps, schema_editor):
    user_model = apps.get_model('bot', 'user')
    settings_model = apps.get_model('bot', 'usersettingsobject')
    for instance in user_model.objects.all():
        # Создаём новый объект в ModelB
        new_b = settings_model.objects.create()
        # Присваиваем его id новому полю в ModelA
        instance.global_settings = new_b
        instance.save()

class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettingsObject',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ping_in_stats', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='chatmember',
            name='local_settings',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.usersettingsobject'),
        ),
        migrations.AddField(
            model_name='user',
            name='global_settings',
            field=models.ForeignKey(default=uuid.uuid4, on_delete=django.db.models.deletion.CASCADE, to='bot.usersettingsobject'),
        ),
        migrations.RunPython(populate_new_field),
    ]
