from django.shortcuts import render
from .models import Container

def containers_list(request):
    containers = Container.objects.all()
    return render(request, 'containers/containers_list.html', {'containers': containers})
