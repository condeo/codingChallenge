from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from datetime import date
from django.core.urlresolvers import reverse
#used for complex numeric operations. Here, we'll just be performing weekdays operations
import numpy as np
import logging
logger = logging.getLogger(__name__)

#signal processors
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
def compute_length_of_service(dropoff, pickup):
    '''
    helper function to compute length of service of a repair
    '''
    try:
        #using numpy to compute difference on only business days
        los = np.busday_count(dropoff,pickup)
        logger.debug('length of service in business days from {} to {} is {}'.format(dropoff,pickup,los))
        return los
    except Exception as e:
        logger.error("exception occured in compute_length_of_service", exc_info=True)

class Mechanic(models.Model):
    '''
    mechanics that perform repairs
    '''
    name = models.CharField(max_length=255)

    class Meta(object):
        verbose_name = 'Mechanic'
        verbose_name_plural = 'Mechanics'
        ordering = ['-name']

    def __unicode__(self):
        return u'%s' % (self.name)
    def get_absolute_url(self):
        return reverse('mechanic_infos', args=[self.id])

class CarRepair(models.Model):
    '''
    captures a car repair job
    '''
    dropoff_date = models.DateField(default=date.today)
    pickup_date = models.DateField(null=True, blank=True)
    assigned_mechanic = models.ForeignKey(
        Mechanic, related_name='related_repairs', null=True, blank=True)
    los = models.IntegerField(null=True, blank=True)
    REPAIR_TYPES = (
        ('A', 'A-oil change'),
        ('B', 'B-tire repair'),
        ('C', 'C-engine inspection'),
        ('D', 'D-tune-up'),
        ('E', 'E-brake service'),
        ('F', 'F-oil gasket replacement'),
    )
    type_of_repair = models.CharField(
        max_length=1,
        choices=REPAIR_TYPES,
        null=True,
    )

    class Meta(object):
        verbose_name = 'repair'
        verbose_name_plural = 'repairs'
        ordering = ['-dropoff_date']
        db_table = 'shop_workflow_fact'

    def __unicode__(self):
        return u'%s -Assigned to: %s' % (self.type_of_repair, self.assigned_mechanic)

    def get_absolute_url(self):
        return reverse('repair_details', args=[self.id])

def repair_pre_save(sender, instance, *args, **kwargs):
    '''
    Signal processor that gets called before a car repair is saved.
    It computes the length of service of each repair
    '''
    if instance.dropoff_date and instance.pickup_date:
        instance.los = compute_length_of_service(instance.dropoff_date, instance.pickup_date)

#ensures that signal is called for only the CarRepair model
models.signals.pre_save.connect(repair_pre_save, sender=CarRepair)