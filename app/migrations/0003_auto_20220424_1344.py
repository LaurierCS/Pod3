# Generated by Django 3.1.13 on 2022-04-24 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20220424_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='deckId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.deck'),
        ),
    ]