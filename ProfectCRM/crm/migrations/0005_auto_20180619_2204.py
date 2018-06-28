# Generated by Django 2.0.5 on 2018-06-19 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20180611_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '未签约'), (1, '已签约')], default=0, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='tags',
            field=models.ManyToManyField(blank=True, to='crm.Tag', verbose_name='标签'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='roles',
            field=models.ManyToManyField(blank=True, to='crm.Role', verbose_name='角色'),
        ),
    ]