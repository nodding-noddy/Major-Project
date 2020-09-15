# Generated by Django 3.0.6 on 2020-05-27 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branch_name', models.CharField(max_length=11)),
                ('branch_code', models.CharField(default='UD', max_length=2, primary_key='True', serialize=False)),
            ],
            options={
                'db_table': 'branch_data',
            },
        ),
        migrations.CreateModel(
            name='Student_data',
            fields=[
                ('roll_no', models.CharField(default='020', max_length=12, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('b_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch', to='register.Branch')),
            ],
            options={
                'db_table': 'student_data',
            },
        ),
    ]