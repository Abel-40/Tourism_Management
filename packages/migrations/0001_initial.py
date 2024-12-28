# Generated by Django 5.1.4 on 2024-12-24 12:15

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=250)),
                ('package_description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('days_of_tour', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('PB', 'Publish'), ('DR', 'Draft')], default='PB', max_length=2)),
                ('location', models.CharField(max_length=100)),
                ('weather', models.CharField(max_length=100)),
                ('landscape', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Packages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-publish'],
                'indexes': [models.Index(fields=['-publish'], name='packages_pa_publish_6c262c_idx')],
            },
        ),
    ]