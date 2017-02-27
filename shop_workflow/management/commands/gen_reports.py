from django.core.management.base import BaseCommand
from shop_workflow.models import CarRepair, Mechanic
import os
from datetime import datetime

import numpy as np
import pandas as pd

class Command(BaseCommand):
    help("typical command would be: python manage.py gen_reports")

    def handle(self, *args, **options):
        # Load database objects into a dataframe
        repairs = CarRepair.objects.all().values('assigned_mechanic__name', 'los',
                                                 'type_of_repair')  # this line can create bottleneck effect
        df = pd.DataFrame.from_records(repairs)
        df.rename(columns={'assigned_mechanic__name': 'Mechanic',
                           'los': 'Avg resp. time', 'type_of_repair': 'repair type'}, inplace=True)
        pivot = pd.pivot_table(df, index=["Mechanic", "repair type"])
        pivot['above National avg.'] = np.where(
            pivot['Avg resp. time'] >= 1, 'yes', 'no')
        # print df
        print pivot
        # process each row
        for row in pivot.itertuples(index=True, name='repair_record'):
            if row[0][1] == 'A' or row[0][1] == 'B':
                pivot['above National avg.'] = np.where(
                    pivot['Avg resp. time'] >= 1, 'yes', 'no')
            if row[0][1] == 'C' or row[0][1] == 'E':
                pivot['above National avg.'] = np.where(
                    pivot['Avg resp. time'] >= 3, 'yes', 'no')
            if row[0][1] == 'D':
                pivot['above National avg.'] = np.where(
                    pivot['Avg resp. time'] >= 2, 'yes', 'no')
            if row[0][1] == 'F':
                pivot['above National avg.'] = np.where(
                    pivot['Avg resp. time'] >= 2.5, 'yes', 'no')
        self.pivot = pivot
    