# Generated by Django 4.2.9 on 2024-02-07 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_alter_publication_site'),
        ('Assessment', '0019_remove_questionpaperformat_question_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionpaperformat',
            name='question_type',
            field=models.ManyToManyField(blank=True, limit_choices_to={'parent__isnull': True}, null=True, to='core.questiontype'),
        ),
    ]
