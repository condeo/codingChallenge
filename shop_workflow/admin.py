from django.contrib import admin
from django.contrib import admin
from shop_workflow.models import CarRepair, Mechanic

# Register your models here.
class CarRepairAdmin(admin.ModelAdmin):
    '''
    admin page display manager for a Car repair
    '''
    list_display = ('id', 'dropoff_date', 'pickup_date',
                    'assigned_mechanic', 'type_of_repair','los')
admin.site.register(CarRepair, CarRepairAdmin)


class MechanicAdmin(admin.ModelAdmin):
    '''
    admin page display manager for a Car repair
    '''
    list_display = ('id', 'name')
admin.site.register(Mechanic, MechanicAdmin)