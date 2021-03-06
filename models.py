from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save


class Subnet(models.Model):
    STATIC = 'Static'
    DHCP = 'DHCP'

    name = models.CharField(
        verbose_name="Subnet Name",
        max_length=100
    )
    vlan = models.IntegerField(
        verbose_name='Vlan Id'
    )
    first_host = models.GenericIPAddressField(
        protocol='IPv4'
    )
    last_host = models.GenericIPAddressField(
        protocol='IPv4'
    )
    cidr = models.CharField(
        verbose_name="CIDR Scope",
        max_length=3,
        default='/24',
        help_text='The CIDR notation for the subnet (ie "/24"). defaults to /24'
    )
    netmask = models.GenericIPAddressField(
        protocol='IPv4',
        default="255.255.255.0"
    )
    broadcast = models.GenericIPAddressField(
        protocol='IPv4'
    )
    dns_1 = models.GenericIPAddressField(
        verbose_name="Primary DNS Server",
        blank=True,
        null=True,
        protocol='IPv4'
    )
    dns_2 = models.GenericIPAddressField(
        verbose_name="Secondary DNS Server",
        blank=True,
        null=True,
        protocol='IPv4'
    )
    gateway = models.GenericIPAddressField(
        verbose_name="Gateway",
        protocol='IPv4'
    )
    last_sweep = models.DateTimeField(
        blank=True,
        null=True,
    )
    SUBNET_TYPE_CHOICES = (
        (STATIC, 'Static'),
        (DHCP, 'DHCP'),
    )
    type = models.CharField(
        verbose_name="Subnet Type",
        max_length=20,
        choices=SUBNET_TYPE_CHOICES,
        default=STATIC,
    )
    dhcp_start = models.GenericIPAddressField(
        blank=True,
        null=True,
        protocol='IPv4',
    )
    dhcp_end = models.GenericIPAddressField(
        blank=True,
        null=True,
        protocol='IPv4',
    )

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = ('Subnet')
        verbose_name_plural = ('Subnets')


class Host(models.Model):
    STATIC = 'Static'
    DHCP_RESERVATION = 'DHCP_RESERVATION'
    DHCP = 'DHCP'
    SUCCESS = 'Success'
    UNDETERMINED = 'Undetermined'
    FAIL = 'Fail'

    address = models.GenericIPAddressField(protocol='IPv4',unique=True)

    subnet = models.ForeignKey(
        Subnet,
        on_delete=models.CASCADE,
    )

    machine_name = models.CharField(
        blank=True,
        null=True,
        max_length=100
    )
    building = models.CharField(
        blank=True,
        null=True,
        max_length=100
    )
    location = models.CharField(
        blank=True,
        null=True,
        max_length=100
    )
    machine_dec = models.TextField(
        verbose_name="Machine Description",
        blank=True,
        null=True,
    )

    ADDRESS_TYPE_CHOICES = (
        (STATIC, 'Static'),
        (DHCP_RESERVATION, 'DHCP Reservation'),
        (DHCP, 'DHCP'),
    )
    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPE_CHOICES,
        default=STATIC,
    )

    eth_port = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Vlan Id',
        default=0,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    PING_STATUS_CHOICES = (
        (SUCCESS, 'Success'),
        (UNDETERMINED, 'Undetermined'),
        (FAIL, 'Failed'),
    )
    ping_status = models.CharField(
        max_length=20,
        choices=PING_STATUS_CHOICES,
        default=UNDETERMINED,
    )

    last_ping = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return "%s" % self.address

    class Meta:
        ordering = ('id',)
        verbose_name = 'Host'
        verbose_name_plural = 'Hosts'


class PingHistory(models.Model):
    SUCCESS = 'Success'
    UNDETERMINED = 'Undetermined'
    FAIL = 'Fail'

    host = models.ForeignKey(Host, on_delete=models.CASCADE)

    PING_STATUS_CHOICES = (
        (SUCCESS, 'Success'),
        (UNDETERMINED, 'Undetermined'),
        (FAIL, 'Failed'),
    )

    ping_status = models.CharField(
        max_length=20,
        choices=PING_STATUS_CHOICES,
        default=UNDETERMINED,
    )

    ping_date = models.DateTimeField(
        blank=True,
        null=True
    )
