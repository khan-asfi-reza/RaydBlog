# Generated by Django 3.2.7 on 2021-10-06 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_uid', models.UUIDField(unique=True)),
                ('device_os_type', models.IntegerField(choices=[(1, 'iOS'), (2, 'Android'), (3, 'BlackBerry Tablet OS'), (4, 'Windows Phone'), (5, 'Windows'), (6, 'BlackBerry OS'), (7, 'Mac OS X'), (8, 'Ubuntu'), (9, 'Symbian OS'), (10, 'Linux'), (11, 'Chrome OS'), (12, 'Harmony OS'), (13, 'Other')])),
                ('device_os_family', models.CharField(max_length=126)),
                ('ip_address', models.CharField(max_length=50)),
                ('first_login', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
