from django.shortcuts import render, get_object_or_404
from .models import Container
from .forms import PostForm
from django.shortcuts import redirect # redirect po dodaniu kontenera
import lxc
import os
import mgmt_cont
import pygal   
from collections import Counter

def mgmt_list():
    cont = []
    for k in lxc.list_containers(as_object=True):
        cont.append(k)
    return cont

def container_delete(request, pk):
    print pk
    container = get_object_or_404(Container, pk=pk)
    print container
    print "DELETED!!!"
    c = lxc.Container(container.name)
    print c.name
    if c.running:
        c.stop()
    if c.destroy():
        Container.objects.filter(name=container.name).delete()
    return redirect('container_delete', pk=container.pk)

def container_stop(request, pk):
    print pk
    container = get_object_or_404(Container, pk=pk)
    print "STOPPED!!!"
    c = lxc.Container(container.name)
    if c.running:
        c.stop()
    return redirect('container_stop', pk=container.pk)

def container_start(request, pk):
    print pk
    container = get_object_or_404(Container, pk=pk)
    print "STARTED!!!"
    c = lxc.Container(container.name)
    if not c.running:
        c.start()
    return redirect('container_start', pk=container.pk)

def containers_list(request):
    containers = Container.objects.all()
    chart = pygal.Pie()
    cnt = {}
    for g in Container.objects.all():
        c = lxc.Container(g.name)
        cnt[g.name] = g.status
        g.status = c.state
        if not c.defined:
            g.status = "UNKNOWN"
        g.save()
    print cnt.values()
    print type(Counter(cnt.values())['RUNNING'])
    val = Counter(cnt.values())['RUNNING']
    chart.add('RUNNING', val)
    val1 = Counter(cnt.values())['STOPPED']
    chart.add('STOPPED', val1)
    val2 = Counter(cnt.values())['UNKNOWN']
    chart.add('UNKNOWN', val2)
    #chart.add('RUNNING', 1)
    chart.render_to_file('./static/bar_chart.svg')
    return render(request, 'containers/containers_list.html', {'containers': containers})

def container_details(request, pk):
    container = get_object_or_404(Container, pk=pk)
    c = lxc.Container(container.name)
    if c.running:
        container.net_ip = c.get_ips()[0]
        container.net_if = c.get_interfaces()[0]
        #name = c.name
        #print os.system("lxc-attach -n 'name' ifconfig eth0 | grep Mask | cut -d\":\" -f4") 
        #container.os_ver = c.attach_wait(lxc.attach_run_command, ["lsb_release -r|awk'{print", "$2}'"])
        #print c.attach_wait(lxc.attach_run_command, ["lsb_release", "-r", "|awk", "'{print", "$2}'"])
    return render(request, 'containers/container_details.html', {'container': container})

def container_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            container = form.save(commit=False)
            c = lxc.Container(container.name)
            c.create("download", 0,{"dist": "ubuntu", "release": "trusty","arch": "amd64"})
            container.save()
            return redirect('container_details', pk=container.pk)
    else:
        form = PostForm()
    return render(request, 'containers/container_edit.html', {'form': form})

def container_edit(request, pk):
    post = get_object_or_404(Container, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            container = form.save(commit=False)
            #z = Container.objects.get(id=pk)
            #x = lxc.Container("test")
            #z.name = x.name
            #z.name = "test"
            #z.net_ip = x.get_ips(timeout=9)[0]
            post.save()
            mgmt_cont.sync(pk)
            #z.save()
            return redirect('container_details', pk=container.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'containers/container_edit.html', {'form': form})
