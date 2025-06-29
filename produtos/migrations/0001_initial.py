# Generated by Django 5.2.2 on 2025-06-11 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fabricante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('cod_embalagem', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('ref_fabricante', models.CharField(max_length=100)),
                ('qtd_entrada', models.IntegerField()),
                ('estoque_minimo', models.IntegerField()),
                ('estoque_maximo', models.IntegerField()),
                ('cod_barra', models.CharField(max_length=50)),
                ('apresentacao', models.CharField(max_length=60)),
                ('situacao', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo', max_length=10)),
                ('data_ultima_compra', models.DateField(blank=True, null=True)),
                ('fabricante', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='produtos.fabricante')),
                ('grupo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='produtos.grupo')),
                ('marca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='produtos.marca')),
            ],
        ),
    ]
