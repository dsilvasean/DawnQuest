# Generated by Django 4.2.9 on 2024-01-25 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShaalaaMiner', '0008_alter_solution_resource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='resource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ShaalaaMiner.questionresource'),
        ),
    ]