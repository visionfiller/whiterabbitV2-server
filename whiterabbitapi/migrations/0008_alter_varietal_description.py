# Generated by Django 4.2.1 on 2023-05-30 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whiterabbitapi', '0007_winebottle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='varietal',
            name='description',
            field=models.TextField(),
        ),
    ]
