# Generated by Django 3.2.5 on 2022-07-09 10:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('djangoProject', '0004_auto_20220708_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asdf',
            name='last_login',
            field=models.DateField(default=datetime.datetime(2022, 7, 9, 10, 34, 54, 778986, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='asdf',
            name='time_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 9, 10, 34, 54, 778986, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='elderlyinfo',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 9, 10, 34, 54, 779983, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='elderlylocation',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 9, 10, 34, 54, 780980, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employeeinfo',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 9, 10, 34, 54, 780980, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='eventinfo',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 9, 10, 34, 54, 781977, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='familyelderlyrelationship',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 9, 10, 34, 54, 782974, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='familyinfo',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 9, 10, 34, 54, 782974, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 9, 10, 34, 54, 782974, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='volunteerinfo',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 9, 10, 34, 54, 783972, tzinfo=utc)),
        ),
    ]
