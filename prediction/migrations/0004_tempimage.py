# Generated by Django 5.0.4 on 2024-04-21 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0003_alter_predictionimage_after_predict_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp_image', models.ImageField(upload_to='temp_img/')),
            ],
        ),
    ]