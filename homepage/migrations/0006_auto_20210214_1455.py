# Generated by Django 3.1.6 on 2021-02-14 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_auto_20210214_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='cust_address',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='cust_city',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='cust_mobile',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='cust_parish',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='cust_tax',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='FL_addr1',
            field=models.CharField(default='x', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='FL_addr2',
            field=models.CharField(default='x', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='FL_city',
            field=models.CharField(default='x', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='FL_phonenumber',
            field=models.CharField(default='x', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='FL_state',
            field=models.CharField(default='x', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='FL_zipcode',
            field=models.CharField(default='x', max_length=100),
        ),
    ]
