admin credentials:
username: root
password: A1234567

Loading CSV file would be: python manage.py load_csv
#this will lookf for a csv file named "seed.csv" inside the data folder

# Assumptions: I considered the column id to be the primary key: In other\ 
words, in the example table given, data from line 4 (Rich) will be \
replaced by data from line 5 (Simone).\If the initial data was not\
mistakenly given, in this case, I will need to change this line\
repair_data,repair_created = CarRepair.objects.get_or_create(id=row.id)\
to this line:
repair_data,repair_created = CarRepair.objects.get_or_create(id=row.id,assigned_mechanic = repair_mechanic)
I