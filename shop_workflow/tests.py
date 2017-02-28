from django.test import TestCase
from .models import Mechanic, CarRepair
from django.core.urlresolvers import reverse
from datetime import datetime
from django.shortcuts import get_object_or_404

# Create your tests here.
class CarRepairTestCase(TestCase):
    def setUp(self):
        test_mechanic = Mechanic.objects.create(name='John Q')
        test_repair = CarRepair()
        test_repair.dropoff_date = datetime.strptime("02/26/2017", "%m/%d/%Y")
        test_repair.pickup_date = datetime.strptime("03/04/2017", "%m/%d/%Y")
        test_repair.assigned_mechanic = test_mechanic
        test_repair.type_of_repair = 'F'
        test_repair.save()

    def test_repair(self):
        '''chek that the repair is successfully created'''
        repairs = CarRepair.objects.all()
        self.assertTrue(repairs.count()>0)

    def test_los(self):
        '''chek the lenght of service for the test_repair in business days'''
        repair_item = get_object_or_404(CarRepair, type_of_repair='F')
        self.assertTrue(repair_item.los==5)
