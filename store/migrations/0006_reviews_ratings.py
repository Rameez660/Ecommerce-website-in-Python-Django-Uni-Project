# Generated by Django 3.0.4 on 2021-06-08 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='ratings',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]