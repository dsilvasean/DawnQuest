# Generated by Django 4.2.9 on 2024-02-09 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_alter_question_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solution', to='core.question'),
        ),
    ]
