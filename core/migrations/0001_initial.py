# Generated by Django 4.2.9 on 2024-01-19 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.IntegerField(choices=[(1, 'Maharashtra')])),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Spider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.IntegerField(choices=[(1, 'EBalbharti')])),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.IntegerField(choices=[(1, 'Mathematics')])),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_orig', models.CharField(max_length=255)),
                ('title_eng', models.CharField(blank=True, max_length=255)),
                ('book_cover', models.URLField()),
                ('book_url', models.URLField()),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.board')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.grade')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subject')),
            ],
        ),
    ]
