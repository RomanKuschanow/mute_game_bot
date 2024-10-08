# Generated by Django 5.0.8 on 2024-09-03 10:00

import datetime
import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Punishment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(default='untitled', max_length=100)),
                ('time', models.DurationField(default=datetime.timedelta(seconds=18000))),
                ('is_public', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.user')),
                ('created_in', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.chat')),
            ],
        ),
        migrations.CreateModel(
            name='RandomChoiceGame',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('min_players_count', models.PositiveIntegerField(default=2, validators=[django.core.validators.MinValueValidator(2)])),
                ('max_players_count', models.PositiveIntegerField(default=6, null=True)),
                ('losers_count', models.PositiveIntegerField(default=1)),
                ('is_creator_playing', models.BooleanField(default=True)),
                ('autostart_at_max_players', models.BooleanField(default=False)),
                ('autostart_operator', models.TextField(default='or')),
                ('autostart_at', models.DateTimeField(default=None, null=True)),
                ('is_opened_to_join', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_random_choice_games', to='bot.chatmember')),
                ('punishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.punishment')),
            ],
        ),
        migrations.CreateModel(
            name='RandomChoiceGamePlayer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('join_at', models.DateTimeField(auto_now_add=True)),
                ('chat_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.chatmember')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.randomchoicegame')),
            ],
        ),
        migrations.CreateModel(
            name='RandomChoiceGameLoser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.randomchoicegameplayer')),
            ],
        ),
        migrations.AddField(
            model_name='randomchoicegame',
            name='players',
            field=models.ManyToManyField(related_name='participated_random_choice_games', through='games.RandomChoiceGamePlayer', to='bot.chatmember'),
        ),
        migrations.CreateModel(
            name='RandomChoiceGameResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('finished_at', models.DateTimeField(auto_now_add=True)),
                ('losers', models.ManyToManyField(through='games.RandomChoiceGameLoser', to='games.randomchoicegameplayer')),
            ],
        ),
        migrations.AddField(
            model_name='randomchoicegameloser',
            name='game_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.randomchoicegameresult'),
        ),
        migrations.AddField(
            model_name='randomchoicegame',
            name='result',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game', to='games.randomchoicegameresult'),
        ),
    ]
