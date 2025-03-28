# Generated by Django 5.1.4 on 2025-01-03 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LarkProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar_url', models.URLField(blank=True, null=True)),
                ('open_id', models.CharField(max_length=255, unique=True)),
                ('access_token', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'lark_profile',
            },
        ),
    ]
