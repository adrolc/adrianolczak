# Generated by Django 4.1.6 on 2023-02-12 14:51

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, upload_to=blog.models.post_directory_path),
        ),
    ]
