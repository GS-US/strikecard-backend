from django.db import models


class State(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Zip(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    state = models.ForeignKey(State, on_delete=models.PROTECT)

    class Meta:
        ordering = ('code',)

    def __str__(self):
        return self.code
