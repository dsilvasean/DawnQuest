# Generated by Django 4.2.9 on 2024-01-25 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShaalaaMiner', '0014_remove_question_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='solution',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='ShaalaaMiner.solution'),
            preserve_default=False,
        ),
    ]
