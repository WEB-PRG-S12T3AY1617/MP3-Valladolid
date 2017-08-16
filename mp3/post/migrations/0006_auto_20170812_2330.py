# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-12 15:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20170812_0240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemoffer',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Post'),
        ),
        migrations.AlterField(
            model_name='itemoffer',
            name='itemO_offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Offer'),
        ),
        migrations.AlterField(
            model_name='moneyoffer',
            name='moneyO_offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Offer'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_pic',
            field=models.ImageField(default='img/posts/default.jpg', upload_to='img/posts/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_pic',
            field=models.ImageField(default='img/user/default.png', upload_to='img/user/'),
        ),
    ]