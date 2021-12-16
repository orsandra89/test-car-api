# Generated by Django 3.2.9 on 2021-12-16 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carobject',
            name='carbrand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.carbrand'),
        ),
        migrations.AlterField(
            model_name='carobject',
            name='carmodel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.carmodel'),
        ),
    ]