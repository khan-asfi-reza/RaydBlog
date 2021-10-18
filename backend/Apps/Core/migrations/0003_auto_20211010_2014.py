# Generated by Django 3.2.7 on 2021-10-10 20:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.model_utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Core', '0002_auto_20211010_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockcategory',
            name='category_name',
            field=models.CharField(max_length=200, verbose_name='Category Name'),
        ),
        migrations.AlterField(
            model_name='blockcategory',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Core.blockcategory', verbose_name='Category Parent'),
        ),
        migrations.CreateModel(
            name='BlockPostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.model_utils.file_location)),
                ('block_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.blockpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
