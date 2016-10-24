from django.conf.urls import url
from . import views


app_name = 'ip_manager'

urlpatterns = [
    url(r'^$', views.subnets_index, name='subnet_index'),
    url(r'^hosts/(?P<subnet>[\w\-]+)', views.host_index, name='host_index'),
    url(r'^ping_host/(?P<host_id>\d+)', views.ping_host, name='ping_host'),
    url(r'^ping_host/', views.ping_host, name='host_ping'),
    url(r'^ping_sweep/(?P<subnet>[\w\-]+)', views.ping_sweep, name='ping_sweep'),
    url(r'^search_subnet/(?P<subnet>[\w\-]+)', views.search_subnet, name='search_subnet'),
    url(r'^find_open_host/(?P<subnet>[\w\-]+)', views.find_open_host, name='find_open_host'),
    url(r'^host_table/(?P<subnet>[\w\-]+)', views.host_table, name='host_table'),
    url(r'^update/host', views.update_host, name='update_host'),
    url(r'^details', views.host_details, name='host_details'),
    url(r'^subnet/new', views.new_subnet, name='new_subnet'),
    url(r'^subnet/table', views.view_subnet_table, name='subnet_table'),
    url(r'^subnet/new_subnet_form', views.new_subnet_form, name='new_subnet_form'),
    url(r'^details_by_name', views.host_details_by_name, name='host_details_by_name'),
]
