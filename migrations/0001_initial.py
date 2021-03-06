# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-09 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.GenericIPAddressField(protocol='IPv4')),
                ('subnet', models.CharField(max_length=100)),
                ('machine_name', models.CharField(max_length=100)),
                ('building', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('machine_dec', models.TextField()),
                ('address_type', models.CharField(choices=[('Static', 'Static'), ('DHCP', 'DHCP Reservation')], default='Static', max_length=2)),
                ('eth_port', models.IntegerField(verbose_name='Vlan Id')),
                ('notes', models.TextField()),
                ('ping_status', models.CharField(choices=[('Static', 'Static'), ('Undetermined', 'Undetermined'), ('Fail', 'Failed')], default='Static', max_length=2)),
                ('last_ping', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Subnet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('vlan', models.IntegerField(verbose_name='Vlan Id')),
                ('first_host', models.GenericIPAddressField(protocol='IPv4')),
                ('last_host', models.GenericIPAddressField(protocol='IPv4')),
                ('cidr', models.CharField(default='/24', help_text='The CIDR notation for the subnet (ie "/24"). defaults to /24', max_length=3)),
                ('netmask', models.GenericIPAddressField(protocol='IPv4')),
                ('broadcast', models.GenericIPAddressField(protocol='IPv4')),
                ('dns_1', models.GenericIPAddressField(protocol='IPv4')),
                ('dns_2', models.GenericIPAddressField(protocol='IPv4')),
                ('gateway', models.GenericIPAddressField(protocol='IPv4')),
                ('last_sweep', models.DateTimeField()),
                ('type', models.CharField(choices=[('Static', 'Static'), ('DHCP', 'DHCP')], default='Static', max_length=2)),
                ('dhcp_range', models.GenericIPAddressField(protocol='IPv4')),
            ],
        ),
    ]
