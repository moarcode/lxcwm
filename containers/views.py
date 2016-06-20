from django.shortcuts import render, get_object_or_404
from .models import Container
from .forms import PostForm
from django.shortcuts import redirect # redirect po dodaniu kontenera
import lxc
import os
import mgmt_cont

def mgmt_list():
    cont = []
    for k in lxc.list_containers(as_object=True):
        cont.append(k)
    return cont
        

def containers_list(request):
    containers = Container.objects.all()
    for g in Container.objects.all():
        c = lxc.Container(g.name)
        g.status = c.state
        if not c.defined:
            g.status = "UNKNOWN"
        g.save()
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

def container_start(request, pk):
    c = lxc.Container("test")
    c.start()
    container = get_object_or_404(Container, pk=pk)
    return redirect('container_action', pk=container.pk)
