# Generated by Django 3.2.1 on 2021-10-11 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tunity', '0002_alter_company_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='ending_day',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='ending_hour',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='salary',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='starting_day',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='starting_hour',
            field=models.CharField(max_length=40, null=True),
        ),
    ]