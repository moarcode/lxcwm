from django.shortcuts import render, get_object_or_404
from .models import Container

def containers_list(request):
    containers = Container.objects.all()
    return render(request, 'containers/containers_list.html', {'containers': containers})

def container_details(request, pk):
    container = get_object_or_404(Container, pk=pk)
    return render(request, 'containers/container_details.html', {'container': container})
