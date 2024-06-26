# Generated by Django 5.0.6 on 2024-06-26 12:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_com', models.TextField(verbose_name='Комментарий')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Время написания')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['content_com'],
            },
        ),
        migrations.AddField(
            model_name='news',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='comments', to='news.comment', verbose_name='Комментарии'),
        ),
    ]
