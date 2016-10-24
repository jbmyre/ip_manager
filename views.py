import arrow
from django.shortcuts import render, HttpResponse, render_to_response
import ipcalc as calc
from .models import Subnet, Host
from django.core.exceptions import ObjectDoesNotExist
import json
import re
import subprocess
from sys import platform
import socket


def subnets_index(request):
    network = Subnet.objects.all()
    subnets = dict(subnets=network)
    return render(request, "ip_manager/subnet_index.html", subnets)


def host_index(request, subnet):
    context = dict(subnet_name=subnet)
    return render(request, "ip_manager/host_index.html", context)


def host_table(request, subnet):
    all_hosts = Host.objects.select_related().filter(subnet__name__exact=subnet).all()
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
    network = Subnet.objects.all()
    subnets = dict(subnets=network)
    return render(request, "ip_manager/subnet_table.html", subnets)


def ping_host(request, host_id):
    """pings a single host"""

    host = Host.objects.get(id=host_id)

    if platform == "linux" or platform == "linux2":

        output = subprocess.Popen(
            ['ping', '-c', '1', '-t', '2', host.address], stdout=subprocess.PIPE
        ).communicate()[0]

        if "unknown host" in output.decode('utf-8'):
            host.ping_status = "Undetermined"
        else:
            if "0" in output.decode('utf-8').split(",")[1]:
                host.ping_status = "Fail"
            else:
                host.ping_status = "Success"
            try:
                socket.gethostbyaddr(host.address)
                host.machine_name = socket.gethostbyaddr(host.address)[0]
            except:
                host.machine_name = host.machine_name
        host.last_ping = arrow.now('local').isoformat()
        host.save()
        return HttpResponse("Ping Complete")

    elif platform == "win32":
        try:
            ping = subprocess.Popen(["ping", "-n", "1", "-w", "200", host.address], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            out, error = ping.communicate()
            if out:
                packet = int(re.findall(r"Lost = (\d+)", out)[0])
                if packet == 0:
                    host.ping_status = "Success"
                else:
                    host.ping_status = "Fail"
                try:
                    socket.gethostbyaddr(host.address)
                    host.machine_name = socket.gethostbyaddr(host.address)[0]
                except:
                    host.machine_name = host.machine_name
                host.last_ping = arrow.now('local').isoformat()
                host.save()
        except subprocess.CalledProcessError:
            print "Couldn't get a ping"
        return HttpResponse("Ping Complete")


def ping_sweep(request, subnet):
    """pings all hosts on a subnet"""
    subnet_log = Subnet.objects.get(name__exact=subnet)
    subnet = Host.objects.select_related().filter(subnet__name__exact=subnet).all()

    if platform == "linux" or platform == "linux2":

        for host in subnet:
            output = subprocess.Popen(
                ['ping', '-c', '1', '-t', '2', host.address], stdout=subprocess.PIPE
            ).communicate()[0]

            if "Access denied" in output.decode('utf-8'):
                return HttpResponse("Ping Sweep Failed")

            elif "unknown host" in output.decode('utf-8'):
                host.ping_status = "Undetermined"
            else:
                if "0" in output.decode('utf-8').split(",")[1]:
                    host.ping_status = "Fail"
                else:
                    host.ping_status = "Success"
            try:
                socket.gethostbyaddr(host.address)
                host.machine_name = socket.gethostbyaddr(host.address)[0]
            except:
                host.machine_name = host.machine_name
            host.last_ping = arrow.now('local').isoformat()
            subnet_log.last_sweep = arrow.now('local').isoformat()
            subnet_log.save()
            host.save()
        return HttpResponse("Ping Sweep Complete")

    elif platform == "win32":
        for host in subnet:
            try:
                ping = subprocess.Popen(
                    ["ping", "-n", "1", "-w", "200", host.address], stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                out, error = ping.communicate()
                if out:
                    packet = int(re.findall(r"Lost = (\d+)", out)[0])
                    if packet == 0:
                        host.ping_status = "Success"
                    else:
                        host.ping_status = "Fail"
                    try:
                        socket.gethostbyaddr(host.address)
                        host.machine_name = socket.gethostbyaddr(host.address)[0]
                    except:
                        host.machine_name = host.machine_name
                    host.last_ping = arrow.now('local').isoformat()
                    host.save()
                    subnet_log.last_sweep = arrow.now('local').isoformat()
                    subnet_log.save()
            except subprocess.CalledProcessError:
                print "Couldn't get a ping"
        return HttpResponse("Ping Sweep Complete")


def new_subnet(request):
    """Create a new subnet object and all its host objects"""
    form = request.POST
    first_host = form.get("first_host")
    cidr = form.get("cidr")
    cidr_notation = '%s%s' % (first_host, cidr)
    s = calc.Network(cidr_notation)
    name = form.get("name")
    name = name.replace(" ", "_")
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

    n.save()
    subnet_obj = Subnet.objects.get(name=name)
    whole_subnet = calc.Network(cidr_notation)

    for host_ip in whole_subnet:
        ip = str(host_ip)
        h = Host(machine_name='', address=ip, subnet=subnet_obj)
        h.save(force_insert=True)
    return HttpResponse("New Subnet created")


def find_open_host(request, subnet):
    host = Host.objects.select_related().filter(
        subnet__name__exact=subnet).filter(
        machine_name='').filter(
        ping_status__exact="Fail"
    ).first()

    details = {'host': host}
    return render(request, "ip_manager/open_host_details.html", details)


def host_details_by_name(request):
    name = request.POST.get("name")
    host = Host.objects.filter(machine_name__exact=name)
    details = {'host': host}
    return render(request, "ip_manager/open_host_details.html", details)


def search_subnet(request, subnet):
    """
        autocomplete suggestions for machine names on a specified subnet.
        :returns json
    """

    hosts = Host.objects.select_related().filter(subnet__name__exact=subnet).all()
    host_dict = {}
    for h in hosts:
        if h.machine_name:
            name = h.machine_name
            host_dict[name] = ''
    results = json.dumps(host_dict)
    return HttpResponse(results, content_type="application/json")

