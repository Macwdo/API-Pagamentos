# Generated by Django 4.1.3 on 2022-11-18 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0005_conta_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='cpf',
            field=models.CharField(max_length=11),
        ),
    ]
