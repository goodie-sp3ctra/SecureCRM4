# apps/dashboard/models.py
from django.db import models
from apps.customers.models import Job


class Job(models.Model):
    title = models.CharField(max_length=100)

class Client(models.Model):
    name = models.CharField(max_length=100)
