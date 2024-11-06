# Generated by Django 5.1.2 on 2024-11-06 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_tablecol_col_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericdata',
            name='double_imag_value',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='tablecol',
            name='col_type',
            field=models.CharField(choices=[('object', 'String'), ('datetime64[ns]', 'datetime'), ('category', 'Category'), ('uint8', 'Unsigned 8 bit Integer'), ('uint16', 'Unsigned 16 bit Integer'), ('uint32', 'Unsigned 32 bit Integer'), ('uint64', 'Unsigned 64 bit Integer'), ('int8', 'Signed 8 bit Integer'), ('int16', 'Signed 16 bit Integer'), ('int32', 'Signed 32 bit Integer'), ('int64', 'Signed 64 bit Integer'), ('float32', '32 bit Floating Number'), ('float64', 'Float64'), ('complex128', 'Complex128'), ('bool', 'Boolean')], max_length=20),
        ),
    ]
