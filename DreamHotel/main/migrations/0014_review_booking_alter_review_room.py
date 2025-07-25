# Generated by Django 5.1.2 on 2024-12-13 16:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_review_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='booking',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main.booking'),
        ),
        migrations.AlterField(
            model_name='review',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main.room'),
        ),
    ]
