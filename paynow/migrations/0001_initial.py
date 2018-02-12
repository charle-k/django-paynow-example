# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaynowPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('cellphone', models.CharField(max_length=100, blank=True)),
                ('reference', models.CharField(max_length=100, blank=True)),
                ('paynow_reference', models.CharField(max_length=100, blank=True)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('additionalinfo', models.CharField(max_length=500, blank=True)),
                ('authemail', models.CharField(max_length=100, blank=True)),
                ('init_status', models.CharField(max_length=10, blank=True)),
                ('pollurl', models.CharField(max_length=500, blank=True)),
                ('browserurl', models.CharField(max_length=500, blank=True)),
                ('creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(max_length=10, blank=True)),
                ('paid', models.BooleanField(default=False)),
                ('confirmed_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
