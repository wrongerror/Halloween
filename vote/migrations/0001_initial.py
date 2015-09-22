# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Designer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u4f5c\u8005\u540d\u79f0')),
                ('phone', models.CharField(max_length=11, unique=True, null=True, verbose_name='\u624b\u673a\u53f7', blank=True)),
                ('address', models.CharField(max_length=256, null=True, verbose_name='\u5730\u5740', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated', db_index=True)),
            ],
            options={
                'verbose_name': '\u4f5c\u8005',
                'verbose_name_plural': '\u4f5c\u8005',
            },
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u4f5c\u54c1\u540d')),
                ('number', models.CharField(max_length=8, verbose_name='\u4f5c\u54c1\u7f16\u53f7')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated', db_index=True)),
                ('designer', models.ForeignKey(related_name='production', verbose_name='\u4f5c\u8005', to='vote.Designer', null=True)),
            ],
            options={
                'verbose_name': '\u4f5c\u54c1',
                'verbose_name_plural': '\u4f5c\u54c1',
            },
        ),
        migrations.CreateModel(
            name='ProductionImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original', models.ImageField(upload_to=b'productions', max_length=255, verbose_name='\u56fe\u7247')),
                ('display_order', models.PositiveIntegerField(default=0, help_text='0\u4ee3\u8868\u4e3b\u56fe', verbose_name='\u663e\u793a\u987a\u5e8f')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('production', models.ForeignKey(related_name='images', verbose_name='\u4f5c\u54c1', to='vote.Production')),
            ],
            options={
                'ordering': ['display_order'],
                'verbose_name': '\u4f5c\u54c1\u56fe\u7247',
                'verbose_name_plural': '\u4f5c\u54c1\u56fe\u7247',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openid', models.CharField(max_length=32, null=True, verbose_name='OpenId', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated', db_index=True)),
                ('production', models.ForeignKey(related_name='votes', verbose_name=b'production', to='vote.Production')),
            ],
            options={
                'verbose_name': '\u6295\u7968\u8bb0\u5f55',
                'verbose_name_plural': '\u6295\u7968\u8bb0\u5f55',
            },
        ),
        migrations.AlterUniqueTogether(
            name='productionimage',
            unique_together=set([('production', 'display_order')]),
        ),
    ]
