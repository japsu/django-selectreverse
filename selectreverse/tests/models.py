from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
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

class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

class Bookmark(models.Model):
    url = models.URLField()
    tags = generic.GenericRelation(TaggedItem)

    objects = models.Manager()
    reversemanager = ReverseManager({'gtags': 'tags'})
    
