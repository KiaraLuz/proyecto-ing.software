# Generated by Django 5.0.7 on 2024-07-30 17:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_receta_recetaingrediente_receta_ingredientes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostoProducto',
            fields=[
                ('id_costo', models.AutoField(primary_key=True, serialize=False)),
                ('costo_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producto')),
            ],
        ),
        migrations.CreateModel(
            name='CostoProductoIngrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_ingrediente', models.DecimalField(decimal_places=2, max_digits=10)),
                ('costo_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('costo_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.costoproducto')),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ingrediente')),
            ],
        ),
        migrations.AddField(
            model_name='costoproducto',
            name='ingredientes',
            field=models.ManyToManyField(through='app.CostoProductoIngrediente', to='app.ingrediente'),
        ),
    ]
