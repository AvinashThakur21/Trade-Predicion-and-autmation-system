# Generated by Django 5.0 on 2024-04-26 05:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('version01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_result', models.TextField()),
                ('trade_summery', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50)),
                ('user_username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('broker', models.CharField(max_length=50)),
                ('api', models.TextField(help_text='api by broker or entry and exit')),
            ],
        ),
        migrations.CreateModel(
            name='user_personalization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_trading', models.BooleanField()),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='stock',
            name='script_id must be unique',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='name',
            new_name='stock_name',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='id',
        ),
        migrations.AlterField(
            model_name='stock',
            name='script_id',
            field=models.AutoField(help_text='Nse script id ', primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='result',
            name='trade_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='version01.trade'),
        ),
        migrations.AddField(
            model_name='user_personalization',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='version01.user'),
        ),
    ]
