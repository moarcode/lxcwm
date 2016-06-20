# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

class Container(models.Model):
    name = models.TextField()
    net_ip = models.GenericIPAddressField()
    net_mask = models.GenericIPAddressField()
    net_if = models.TextField()
    mem = models.IntegerField()
    cpu = models.IntegerField()
    os_type = models.TextField()
    os_ver = models.TextField()
    status = models.TextField(default="UNKNOWN")

    def create(self):
        self.create_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name
