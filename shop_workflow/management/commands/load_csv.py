from django.core.management.base import BaseCommand
from shop_workflow.models import CarRepair,Mechanic
import os
from datetime import datetime
# Retrieve current working directory (`cwd`)
cwd = os.getcwd() #current working directory (root of the project)
print 'current working directory is {0}'.format(cwd)
#pandas in order to process csv files effisciently
import pandas as pd

class Command(BaseCommand):
    help("typical command would be: python manage.py load_csv")
    def handle(self, *args, **options):
        # Load csv in a dataframe
        df = pd.read_csv(cwd +"/shop_workflow/data/seed.csv")
        #process each row
        for row in df.itertuples(index=True, name='repair_record'):
            repair_mechanic,mechanic_created = Mechanic.objects.get_or_create(name=row.mechanic)
            repair_data,repair_created = CarRepair.objects.get_or_create(id=row.id)
            repair_data.dropoff_date = datetime.strptime(row.dropoff, "%m/%d/%Y") #converts string  dd/mm/yyyy to date
            repair_data.pickup_date = datetime.strptime(row.pickup, "%m/%d/%Y")
            repair_data.assigned_mechanic = repair_mechanic
            repair_data.type_of_repair = row.RepairType
            repair_data.save()
            print repair_data
