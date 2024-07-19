# Generated by Django 5.0.7 on 2024-07-19 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_unidadesmedida'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_producto', models.CharField(max_length=100)),
                ('estado_producto', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductoIngrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ingrediente')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producto')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='ingredientes',
            field=models.ManyToManyField(through='app.ProductoIngrediente', to='app.ingrediente'),
        ),
    ]
