# Generated by Django 5.1.4 on 2024-12-29 15:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_alter_booking_status'),
        ('packages', '0007_alter_packages_package_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.UniqueConstraint(fields=('user', 'package'), name='unique_user_package_booking'),
        ),
    ]