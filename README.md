##Ip Manager

Django app to manage IP addresses and subnets.

###Requirements:
<ul>
<li>python 2.7 +</li>
<li>django 1.9 +</li>
<li>ipcalc</li>
<li>arrow</li>
</ul>


###Install 

'''pip install ipcalc arrow'''

add 'ip_manager' to INSTALLED_APPS in settings.py

add 'url(r'^ip_manager/', include('ip_manager.urls', namespace="ip_manager")),' to urls.py

run '''./manage.py collectstatic'''

run '''./manage.py migrate'''


###Features

Pings hosts or entire subnets, from the browser or on a cron schedule.

Keeps a history of all ping attempts, history can be reviewed in pretty charts.

The ping functionality only works on linux or osx at the moment.

Find an open ip on a subnet.

Material design

