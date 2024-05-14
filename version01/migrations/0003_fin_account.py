# Generated by Django 5.0 on 2024-05-02 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('version01', '0002_fin_account_result_user_user_personalization_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='fin_account',
            fields=[
                ('wallet_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_ammount', models.FloatField()),
                ('total_loss', models.FloatField()),
                ('total_pnl', models.FloatField()),
            ],
        ),
    ]
