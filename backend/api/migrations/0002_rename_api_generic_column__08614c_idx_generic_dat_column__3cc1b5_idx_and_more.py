# Generated by Django 5.1.2 on 2024-11-01 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='genericdata',
            new_name='generic_dat_column__3cc1b5_idx',
            old_name='api_generic_column__08614c_idx',
        ),
        migrations.RenameIndex(
            model_name='tablecol',
            new_name='table_col_file_id_ad29af_idx',
            old_name='api_tableco_file_id_93f0d4_idx',
        ),
        migrations.AlterModelTable(
            name='genericdata',
            table='generic_data',
        ),
        migrations.AlterModelTable(
            name='tablecol',
            table='table_col',
        ),
    ]
