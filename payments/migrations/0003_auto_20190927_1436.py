# Generated by Django 2.2.5 on 2019-09-27 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20190927_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paynowpayment',
            name='authemail',
        ),
        migrations.AddField(
            model_name='paynowpayment',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
