# Generated by Django 3.2.7 on 2021-10-10 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockcomment',
            name='reactions',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='blockpost',
            name='reactions',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
