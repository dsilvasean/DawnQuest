# Generated by Django 4.2.9 on 2024-03-03 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_question_custom_question_note_question_visibility'),
        ('Assessment', '0022_alter_questionpaperformat_question_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionpaperformat',
            name='question_type',
            field=models.ManyToManyField(blank=True, limit_choices_to={'numchild': 0}, null=True, to='core.corequestiontype'),
        ),
    ]