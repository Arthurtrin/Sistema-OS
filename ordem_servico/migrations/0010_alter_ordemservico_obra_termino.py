# Generated by Django 5.0.6 on 2025-07-11 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordem_servico', '0009_alter_ordemservico_n_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemservico',
            name='obra_termino',
            field=models.DateField(null=True),
        ),
    ]
