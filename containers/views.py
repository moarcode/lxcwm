from django.shortcuts import render, get_object_or_404
from .models import Container
from .forms import PostForm
from django.shortcuts import redirect # redirect po dodaniu kontenera

def containers_list(request):
    containers = Container.objects.all()
    return render(request, 'containers/containers_list.html', {'containers': containers})

def container_details(request, pk):
    container = get_object_or_404(Container, pk=pk)
    return render(request, 'containers/container_details.html', {'container': container})

def container_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            container = form.save(commit=False)
            #container.author = request.user
            #container.published_date = timezone.now()
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
            #post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('container_detail', pk=container.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'containers/container_edit.html', {'form': form})

