# Generated by Django 5.1.2 on 2024-12-25 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_guestprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guestprofile',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='profile_pictures/'),
        ),
    ]
