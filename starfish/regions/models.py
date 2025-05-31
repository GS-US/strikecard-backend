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
    type = models.CharField(max_length=20)
    primary_city = models.CharField(max_length=100, blank=True, null=True)
    acceptable_cities = models.TextField(blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    area_codes = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('code',)
        verbose_name = 'ZIP Code'

    def __str__(self):
        return f'{self.code} {self.state}'
