from django import forms


class NewSubnetForm(forms.Form):
    STATIC = 'Static'
    DHCP = 'DHCP'
    SUBNET_TYPE_CHOICES = (
        (STATIC, 'Static'),
        (DHCP, 'DHCP'),
    )
    name = forms.CharField(
        label='Subnet Name', max_length=100
    )
    first_host = forms.GenericIPAddressField(
        label="Base Ip Address",

    )
    vlan = forms.IntegerField(
        label='Vlan Number'
    )
    cidr = forms.CharField(
        label='Scope', max_length=100
    )
    netmask = forms.GenericIPAddressField(
        label="Netmask",
    )
    gateway = forms.GenericIPAddressField(
        label="Gateway IP"
    )
    dns1 = forms.GenericIPAddressField(
        label="Primary DNS IP"
    )
    dns2 = forms.GenericIPAddressField(
        label="Secondary DNS IP"
    )
    type = forms.ChoiceField(
        SUBNET_TYPE_CHOICES
    )

