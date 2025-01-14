# Generated by Django 5.1.4 on 2024-12-25 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train_scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainstation',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='train',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2),
        ),
        migrations.AlterField(
            model_name='trainlog',
            name='description',
            field=models.TextField(),
        ),
    ]
