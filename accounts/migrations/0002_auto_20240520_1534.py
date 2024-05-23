# Generated by Django 3.2.25 on 2024-05-20 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='nickname',
        ),
        migrations.RemoveField(
            model_name='user',
            name='age',
        ),
        migrations.RemoveField(
            model_name='user',
            name='deposit_period',
        ),
        migrations.RemoveField(
            model_name='user',
            name='desire_amount_deposit',
        ),
        migrations.RemoveField(
            model_name='user',
            name='desire_amount_saving',
        ),
        migrations.RemoveField(
            model_name='user',
            name='financial_products',
        ),
        migrations.RemoveField(
            model_name='user',
            name='money',
        ),
        migrations.RemoveField(
            model_name='user',
            name='salary',
        ),
        migrations.RemoveField(
            model_name='user',
            name='saving_period',
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
    ]