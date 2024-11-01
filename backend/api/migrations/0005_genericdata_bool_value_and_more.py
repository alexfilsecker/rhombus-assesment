# Generated by Django 5.1.2 on 2024-11-01 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_int_sign_genericdata_int_sign_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericdata',
            name='bool_value',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='genericdata',
            name='datetime_value',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='genericdata',
            name='double_value',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='genericdata',
            name='int_sign_value',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='genericdata',
            name='string_value',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='genericdata',
            name='time_zone_info_value',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='genericdata',
            name='uint_value',
            field=models.PositiveBigIntegerField(null=True),
        ),
    ]