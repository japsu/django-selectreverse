# -*- coding: utf-8 -*-

from django import test
from django.conf import settings
import selectreverse.tests.models as test_models
from django.db import connection,  reset_queries
from django.core.exceptions import ImproperlyConfigured

class Test_m2m(test.TestCase):
    def setUp(self):
        settings.DEBUG = True

        for i in range(10):
            o = test_models.Owner(name='Joe')
            o.save()

        for i in range(20):
            a = test_models.Building(number= i)
            a.save()
            a.owners.add(o)

            for j in range(5):
                b = test_models.Appartment(building=a,   number = i*10+j)
                b.save()
                c = test_models.Parking(building=a,  number=i*10+j)
                c.save()

    def test_config(self):
        def testfunc():
            for x in test_models.Building.reversemanager.select_reverse({'owners': 'owners'}):
                pass

        self.assertRaises(ImproperlyConfigured, testfunc)

    def test_reverseFK(self):
        reset_queries()
        for item in test_models.Building.objects.all():
            for x in item.appartment_set.all():
                a = x.number
            for x in item.parking_set.all():
                a = x.number
        self.assertEqual(len(connection.queries), 41)

        reset_queries()
        # all includes all default mappings, as defined in the manager initialisation
        for item in test_models.Building.reversemanager.all():
            for x in getattr(item,  'appartments'):
                a = x.number
            for x in getattr(item,  'parkings'):
                a = x.number
        self.assertEqual(len(connection.queries), 4)

        reset_queries()
        for item in test_models.Building.reversemanager.select_reverse({'appartments': 'appartment_set'}):
            for x in getattr(item,  'appartments'):
                a = x.number
        self.assertEqual(len(connection.queries), 2)

        reset_queries()
        for item in test_models.Building.reversemanager.select_reverse({'parkings': 'parking_set'}):
            for x in getattr(item,  'parkings'):
                a = x.number
        self.assertEqual(len(connection.queries), 2)

	# test select_reverse works on a filtered set
        reset_queries()
        for item in test_models.Building.reversemanager.filter(number__lt = 5).select_reverse({'parkings': 'parking_set'}):
            for x in getattr(item,  'parkings'):
                a = x.number
        self.assertEqual(len(connection.queries), 2)

    def test_m2m(self):
        reset_queries()
        for item in test_models.Building.objects.all():
            for x in item.owners.all():
                a = x.name
        self.assertEqual(len(connection.queries), 21)

        reset_queries()
        # all includes all default mappings, as defined in the manager initialisation
        for item in test_models.Building.reversemanager.all():
            for x in getattr(item,  'xowners'):
                a = x.name
        self.assertEqual(len(connection.queries), 4)

        reset_queries()
        for item in test_models.Building.reversemanager.select_reverse({'xowners': 'owners'}):
            for x in getattr(item,  'xowners'):
                a = x.name
        self.assertEqual(len(connection.queries), 2)

	# test select_reverse works on a filtered set
        reset_queries()
        for item in test_models.Building.reversemanager.filter(number__lt = 5).select_reverse({'xowners': 'owners'}):
            for x in getattr(item,  'xowners'):
                a = x.name
        self.assertEqual(len(connection.queries), 2)

    def test_reversem2m(self):
        reset_queries()
        for item in test_models.Owner.objects.all():
            for x in item.building_set.all():
                a = x.number
        self.assertEqual(len(connection.queries), 11)

        reset_queries()
        # all includes all default mappings, as defined in the manager initialisation
        for item in test_models.Owner.reversemanager.all():
            for x in getattr(item,  'buildings'):
                a = x.number
        self.assertEqual(len(connection.queries), 2)

        reset_queries()
        for item in test_models.Owner.reversemanager.select_reverse({'buildings': 'building_set'}):
            for x in getattr(item,  'buildings'):
                a = x.number
        self.assertEqual(len(connection.queries), 2)

	# test select_reverse works on a filtered set
        reset_queries()
        for item in test_models.Owner.reversemanager.filter(pk__lt = 5).select_reverse({'buildings': 'building_set'}):
            for x in getattr(item,  'buildings'):
                a = x.number
        self.assertEqual(len(connection.queries), 2)

    # you can filter further on a set with select_reverse defined
        reset_queries()
        for item in test_models.Owner.reversemanager.select_reverse({'buildings': 'building_set'}).filter(pk__lt = 5):
            for x in getattr(item,  'buildings'):
                a = x.number
        self.assertEqual(len(connection.queries), 2)

