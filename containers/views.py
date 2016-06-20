from django.shortcuts import render, get_object_or_404
from .models import Container
from .forms import PostForm
from django.shortcuts import redirect # redirect po dodaniu kontenera
import lxc
import mgmt_cont

def mgmt_list():
    cont = []
    for k in lxc.list_containers(as_object=True):
        cont.append(k)
    return cont
        

def containers_list(request):
    cont = []
    containers = Container.objects.all()
    for k in lxc.list_containers(as_object=True):
        cont.append(k)
    for g in Container.objects.all():
        #z = Container.objects.get(g.name)
        #x = lxc.Container(g.name)
        #x = lxc.Container(g.name)
        c = lxc.Container(g.name)
        g.os_type = c.state
        if not c.defined:
            g.os_type = "UNKNOWN"
        #g.name = x.state
        g.save()
        print g.name
    return render(request, 'containers/containers_list.html', {'containers': containers, 'cont': cont})

def container_details(request, pk):
    container = get_object_or_404(Container, pk=pk)
    return render(request, 'containers/container_details.html', {'container': container})

def container_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            container = form.save(commit=False)
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
