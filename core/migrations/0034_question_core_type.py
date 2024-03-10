# Generated by Django 4.2.9 on 2024-02-16 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_corequestiontype'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='core_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question', to='core.corequestiontype'),
        ),
    ]