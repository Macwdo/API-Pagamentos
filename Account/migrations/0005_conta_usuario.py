# Generated by Django 4.1.3 on 2022-11-18 13:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Account', '0004_conta_alter_transferencia_origem_delete_usuarios'),
    ]

    operations = [
        migrations.AddField(
            model_name='conta',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
