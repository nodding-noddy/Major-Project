# Generated by Django 3.0.6 on 2020-05-30 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0005_auto_20200529_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='branch_name',
            field=models.CharField(max_length=25),
        ),
    ]