# Generated by Django 3.1.7 on 2021-03-28 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('line_id', models.CharField(max_length=100)),
                ('handle_squad_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('squad_id', models.IntegerField()),
                ('member_report_status', models.CharField(max_length=200)),
                ('report_title', models.TextField(blank=True)),
                ('report_info', models.TextField(blank=True)),
                ('report_datetime', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Squad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('squad_id', models.IntegerField()),
                ('member_num', models.IntegerField(blank=True)),
                ('member_id', models.CharField(blank=True, max_length=200)),
                ('line_group_id', models.CharField(blank=True, max_length=100)),
                ('line_group_name', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
