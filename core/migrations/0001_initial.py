# Generated by Django 5.2.4 on 2025-07-08 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IPAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(unique=True)),
                ('attempts', models.IntegerField(default=0)),
                ('last_attempt', models.DateTimeField(auto_now=True)),
                ('blocked', models.BooleanField(default=False)),
                ('blocked_until', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
