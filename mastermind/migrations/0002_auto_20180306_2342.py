# Generated by Django 2.0.2 on 2018-03-06 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='num_choices',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='game',
            name='num_pegs',
            field=models.IntegerField(default=4),
        ),
        migrations.AlterField(
            model_name='game',
            name='state',
            field=models.CharField(choices=[('NEW', 'New'), ('STARTED', 'Started'), ('COMPLETED', 'Completed')], default='NEW', max_length=32),
        ),
    ]
