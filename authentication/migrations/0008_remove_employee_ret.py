# Generated by Django 4.2.1 on 2023-05-17 02:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_employee_deduction_employee_ret_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='ret',
        ),
    ]
