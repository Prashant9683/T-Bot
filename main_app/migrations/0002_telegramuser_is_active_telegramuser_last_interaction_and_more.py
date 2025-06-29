# Generated by Django 5.2.3 on 2025-06-25 15:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='last_interaction',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='BotInteraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interaction_type', models.CharField(choices=[('command', 'Command'), ('callback', 'Callback'), ('message', 'Message')], max_length=20)),
                ('command_or_data', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('telegram_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.telegramuser')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='BroadcastMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('total_recipients', models.IntegerField(default=0)),
                ('successful_sends', models.IntegerField(default=0)),
                ('failed_sends', models.IntegerField(default=0)),
                ('is_sent', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
