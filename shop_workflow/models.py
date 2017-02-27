from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from datetime import date
from django.core.urlresolvers import reverse
#used for complex numeric operations. Here, we'll just be performing weekdays operations
import numpy as np

#signal processors
from django.db.models.signals import pre_save
from django.dispatch import receiver

# python loggins
import logging
today_date = datetime.now().strftime("%m-%d-%Y")
extension = 'log'
writepath = 'logs/models_logs{0}.{1}'.format(today_date, extension)
logger = logging.getLogger('model_logs')
hdlr = logging.FileHandler(writepath)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

# Create your models here.
def compute_length_of_service(dropoff, pickup):
    '''
    helper function to compute length of service of a repair
    '''
    try:
        #using numpy to compute difference on only business days
        los = np.busday_count(dropoff,pickup)
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

    def save_from_csv(self, *args, **kwargs):
        '''
        used to save a record from a csv file
        '''
        try:
            repair_mechanic = Mechanic.objects.get_or_create(name=mechanic_name)
            self.dropoff_date = dropoff
            self.pickup_date = pickup
            self.assigned_mechanic = repair_mechanic
            self.type_of_repair = repair_char
            if self.pickup_date > self.dropoff_date:
                self.los = compute_length_of_service(self.dropoff_date, self.pickup_date)
            super(CarRepair, self).save(*args, **kwargs)
        except Exception as e:
            logger.error("exception occured in create_repair", exc_info=True)

def repair_pre_save(sender, instance, *args, **kwargs):
    '''
    Signal processor that gets called before a car repair is saved.
    It computes the length of service of each repair
    '''
    if instance.dropoff_date and instance.pickup_date:
        instance.los = compute_length_of_service(instance.dropoff_date, instance.pickup_date)

#ensures that signal is called for only the CarRepair model
models.signals.pre_save.connect(repair_pre_save, sender=CarRepair)
