# Generated by Django 4.2.17 on 2024-12-15 04:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_name', models.CharField(blank=True, max_length=30, null=True)),
                ('service', models.CharField(blank=True, max_length=100, null=True)),
                ('scheduled_date', models.DateField(blank=True, null=True)),
                ('scheduled_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=False, null=True)),
                ('cancelled', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_services', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('middle_initial', models.CharField(blank=True, max_length=2, null=True)),
                ('mobile_no', models.CharField(blank=True, max_length=15, null=True)),
                ('onboarding_complete', models.BooleanField(default=False)),
                ('account_type', models.CharField(blank=True, default='client', max_length=10, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_name', models.CharField(blank=True, max_length=30, null=True)),
                ('pet_type', models.CharField(blank=True, max_length=30, null=True)),
                ('pet_breed', models.CharField(blank=True, max_length=30, null=True)),
                ('pet_sex', models.CharField(blank=True, max_length=30, null=True)),
                ('pet_age', models.IntegerField(blank=True, null=True)),
                ('pet_birthday', models.DateField(blank=True, null=True)),
                ('pet_condition', models.CharField(blank=True, max_length=30, null=True)),
                ('pet_health', models.CharField(blank=True, max_length=30, null=True)),
                ('pet_weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('notif_type', models.CharField(blank=True, max_length=30, null=True)),
                ('read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
