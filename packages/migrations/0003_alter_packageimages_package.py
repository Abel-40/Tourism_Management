# Generated by Django 5.1.4 on 2025-01-09 07:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packageimages',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_images', to='packages.packages'),
        ),
    ]
