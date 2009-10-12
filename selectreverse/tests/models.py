from django.db import models
from selectreverse.utils import ReverseManager

class Building(models.Model):
    number = models.IntegerField()
    owners = models.ManyToManyField('Owner')
    
    objects = models.Manager()
    reversemanager = ReverseManager({'appartments': 'appartment_set',  'parkings': 'parking_set',  'xowners': 'owners'})

class Appartment(models.Model):
    number = models.IntegerField()
    building = models.ForeignKey(Building)


class Parking(models.Model):
    number = models.IntegerField()
    building = models.ForeignKey(Building)

class Owner(models.Model):
    name = models.CharField(max_length = 50)
    
    objects = models.Manager()
    reversemanager = ReverseManager({'buildings': 'building_set'})
