# Generated by Django 3.1.5 on 2021-05-05 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='psicologo',
            name='name',
            field=models.CharField(default=False, max_length=50),
        ),
    ]
