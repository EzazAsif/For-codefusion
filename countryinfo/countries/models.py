from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    cca2 = models.CharField(max_length=2, unique=True)
    capital = models.CharField(max_length=100, blank=True)
    population = models.BigIntegerField()
    timezones = models.JSONField(default=list)
    languages = models.JSONField(default=dict)
    region = models.CharField(max_length=50)
    flag_url = models.URLField(max_length=255, blank=True)

    def __str__(self):
        return self.name
