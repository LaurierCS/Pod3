# Generated by Django 3.1.13 on 2022-06-09 20:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_auto_20220512_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='deck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.deck'),
        ),
        migrations.AlterField(
            model_name='cardledger',
            name='deck',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.deck'),
        ),
        migrations.AlterField(
            model_name='cardledger',
            name='user_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='deck',
            name='user_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]