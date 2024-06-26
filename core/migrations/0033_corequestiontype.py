# Generated by Django 4.2.9 on 2024-02-16 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_questiontype_marks'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoreQuestionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=155)),
                ('marks', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
