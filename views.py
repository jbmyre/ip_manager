import subprocess
import arrow
from django.shortcuts import render, HttpResponse
import ipcalc as calc
from .models import Subnet, Host
from django.core.exceptions import ObjectDoesNotExist
import json
#from .forms import NewSubnetForm


def subnets_index(request):
    network = Subnet.objects.all()
    subnets = dict(subnets=network)
    return render(request, "ip_manager/subnet_index.html", subnets)


def host_index(request, subnet):
    context = dict(subnet_name=subnet)
    return render(request, "ip_manager/host_index.html", context)


def host_table(request, subnet):
    all_hosts = Host.objects.filter(subnet=subnet).all()
    hosts = dict(hosts=all_hosts, subnet=subnet)
    return render(request, "ip_manager/host_table.html", hosts)


def new_subnet_form(request):
    return render(request, "ip_manager/new_subnet_form_html.html")


def host_details(request):
    ip = request.POST.get("ip")
    host_object = Host.objects.filter(address__exact=ip).all()
    details = {'host': host_object}
    return render(request, "ip_manager/host_details.html", details)


def update_host(request):
    form = request.POST
    address = form.get("address")
    try:
        computer = Host.objects.get(address=address)
        computer.machine_name = form.get("name")
        computer.machine_dec = form.get("machine_dec")
        computer.building = form.get("building")
        computer.location = form.get("location")
        computer.notes = form.get("notes")
        computer.eth_port = form.get("eth_port")
        computer.save()
        message = dict(msg="Successfully Updated host", css="green white-text")
        return HttpResponse(json.dumps(message), content_type="application/json")
    except ObjectDoesNotExist:
        message = dict(msg="Could Not Update Host", css="red white-text")
        return HttpResponse(json.dumps(message), content_type="application/json")


def view_subnet_table(request):
    """
    Return all hosts' details on a requested subnet in a HTML table.
    """

    return request


def single_host_ping(request, ip):
    """pings a single host"""
    print ip
    host = Host.objects.get(id=ip)
    output = subprocess.Popen(['ping', '-c', '1', '-t', '2', host.address], stdout=subprocess.PIPE).communicate()[0]
    print output.decode('utf-8')
    if "unknown host" in output.decode('utf-8'):
        host.ping_status = "Undetermined"
    else:
        if "0" in output.decode('utf-8').split(",")[1]:
            host.ping_status = "Failed"
        else:
            host.ping_status = "Successful"
    host.last_ping = arrow.now('local').isoformat()
    host.save()
    return HttpResponse("ok")


def new_subnet(request):
    """Create a new subnet object and all its host objects"""
    form = request.POST
    first_host = form.get("first_host")
    cidr = form.get("cidr")
    cidr_notation = '%s%s' % (first_host, cidr)
    s = calc.Network(cidr_notation)

    name = form.get("name")
    vlan = form.get("vlan")
    first = str(s.host_first())
    last = str(s.host_last())
    netmask = str(s.netmask())
    dns1 = form.get("dns1")
    dns2 = form.get("dns2")
    gateway = form.get("gateway")
    broadcast = str(s.broadcast())

    n = Subnet(
        name=name,
        vlan=vlan,
        first_host=first,
        last_host=last,
        netmask=netmask,
        broadcast=broadcast,
        dns_1=dns1,
        dns_2=dns2,
        gateway=gateway,
    )

    n.save(force_insert=True)

    for host_ip in calc.Network(cidr_notation):
        ip = str(host_ip)
        h = Host(address=ip, subnet=name)
        h.save(force_insert=True)
    return HttpResponse("ok")
