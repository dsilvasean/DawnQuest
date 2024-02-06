# Generated by Django 4.2.9 on 2024-02-03 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_rename_child_questiontype_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='questiontype',
            name='depth',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questiontype',
            name='numchild',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='questiontype',
            name='path',
            field=models.CharField(default=1, max_length=255,),
            preserve_default=False,
        ),
    ]
