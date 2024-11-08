# Generated by Django 5.0.4 on 2024-04-23 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0006_rename_beforepredictionimage_previewpredictionimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='OriginalSizePredictionImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('before_predict', models.ImageField(upload_to='img_original/')),
            ],
        ),
        migrations.RenameModel(
            old_name='PreviewPredictionImage',
            new_name='BeforePredictionImage',
        ),
    ]
