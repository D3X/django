from django.db import models


class MyModel(models.Model):
    x = models.PositiveIntegerField()
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
