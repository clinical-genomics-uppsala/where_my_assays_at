# Generated by Django 3.1.7 on 2021-03-17 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_choice_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enzyme',
            name='assay',
        ),
        migrations.RemoveField(
            model_name='enzyme',
            name='enzyme',
        ),
        migrations.AddField(
            model_name='assaytype',
            name='enzyme',
            field=models.ManyToManyField(help_text='Select enzymes for this assay', to='app.Enzyme'),
        ),
        migrations.AddField(
            model_name='enzyme',
            name='name',
            field=models.CharField(choices=[('A1', 'Alui'), ('C1', 'Cviqi'), ('D2', 'Dpnii'), ('Ha3', 'Haeiii'), ('Hi3', 'Hindiii'), ('Mse1', 'Msei'), ('Msp1', 'Mspi'), ('S1', 'Smai')], default='aa', help_text='Enter enzyme (max 4 chars?)', max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assaylot',
            name='lot',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
