# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('net_ip', models.GenericIPAddressField()),
                ('net_mask', models.GenericIPAddressField()),
                ('net_if', models.TextField()),
                ('mem', models.IntegerField()),
                ('cpu', models.IntegerField()),
                ('os_type', models.TextField()),
                ('os_ver', models.TextField()),
            ],
        ),
    ]
