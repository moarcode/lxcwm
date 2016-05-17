from django import forms

from .models import Container

class PostForm(forms.ModelForm):

    class Meta:
        model = Container
        fields = ('name', 'mem', 'cpu', 'os_type', 'os_ver', 'net_ip', 'net_mask', 'net_if', )
