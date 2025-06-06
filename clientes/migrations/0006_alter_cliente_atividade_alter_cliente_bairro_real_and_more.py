# Generated by Django 5.2.1 on 2025-06-04 00:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0005_cliente_atividade_cliente_bairro_cobranca_and_more'),
        ('principal', '0003_rename_atividade_atividade_nome_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='atividade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='principal.atividade'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='bairro_real',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cep_real',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cidade_real',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='complemento_real',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='estado_real',
            field=models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], default='-', max_length=2),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='logradouro_real',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='numero_real',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='segmento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='principal.segmento'),
        ),
    ]
