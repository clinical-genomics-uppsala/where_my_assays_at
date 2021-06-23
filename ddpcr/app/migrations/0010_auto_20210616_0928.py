# Generated by Django 3.1.7 on 2021-06-16 07:28

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210616_0904'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assaytype',
            old_name='enzyme',
            new_name='enzymes',
        ),
        migrations.AlterField(
            model_name='assaylot',
            name='date_activated',
            field=models.DateTimeField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=django.utils.timezone.now, message='Make sure the date is not in the future. Todays date is <function now at 0x7fa8603600d0>')], verbose_name='date activated'),
        ),
        migrations.AlterField(
            model_name='assaylot',
            name='date_inactivated',
            field=models.DateTimeField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=django.utils.timezone.now, message='Make sure the date is not in the future. Todays date is <function now at 0x7fa8603600d0>')], verbose_name='date inactivated'),
        ),
        migrations.AlterField(
            model_name='assaylot',
            name='date_order',
            field=models.DateTimeField(validators=[django.core.validators.MaxValueValidator(limit_value=django.utils.timezone.now, message='Make sure the date is not in the future. Todays date is <function now at 0x7fa8603600d0>')], verbose_name='date ordered'),
        ),
        migrations.AlterField(
            model_name='assaylot',
            name='date_scanned',
            field=models.DateTimeField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=django.utils.timezone.now, message='Make sure the date is not in the future. Todays date is 2021-06-16 07:28:24.096902+00:00')], verbose_name='date scanned'),
        ),
        migrations.AlterField(
            model_name='assaylot',
            name='date_validated',
            field=models.DateTimeField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=django.utils.timezone.now, message='Make sure the date is not in the future. Todays date is <function now at 0x7fa8603600d0>')], verbose_name='date validated'),
        ),
        migrations.AlterField(
            model_name='assaypatient',
            name='date_added',
            field=models.DateTimeField(null=True, validators=[django.core.validators.MaxValueValidator(limit_value=django.utils.timezone.now, message='Make sure the date is not in the future. Todays date is <function now at 0x7fa8603600d0>')], verbose_name='date added'),
        ),
    ]