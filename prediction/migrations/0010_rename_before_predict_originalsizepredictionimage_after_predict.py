# Generated by Django 5.0.4 on 2024-04-23 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0009_alter_compressedpredictionimage_after_predict_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='originalsizepredictionimage',
            old_name='before_predict',
            new_name='after_predict',
        ),
    ]