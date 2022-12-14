# Generated by Django 4.1.3 on 2022-11-16 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instituicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_instituicao', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('conta', models.FloatField(default=0)),
                ('instituicao', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Account.instituicao')),
            ],
        ),
        migrations.CreateModel(
            name='Transferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destino', models.CharField(max_length=11)),
                ('valor', models.FloatField()),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('origem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account.usuarios')),
            ],
        ),
    ]
