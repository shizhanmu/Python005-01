# Generated by Django 2.2.13 on 2020-12-23 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Short',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_id', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=100)),
                ('nickname', models.CharField(max_length=100)),
                ('rating', models.CharField(max_length=10)),
                ('posttime', models.DateTimeField()),
                ('shorttext', models.TextField()),
            ],
            options={
                'verbose_name': '短评',
                'verbose_name_plural': '短评',
                'ordering': ['-posttime'],
            },
        ),
    ]
