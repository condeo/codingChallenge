A- To load csv data into MySQL Database, type 
#$python manage.py load_csv
B- To generate and print the report from database records into the shell screen, type 
#$python manage.py gen_reports
C- To run test cases, type 
#$python manage.py test
 
 
0 please create your virtual environment using requirements.txt and activate your virtual environment
    in my case, the virtualEnvironment created was called codingChallenge
1- create a MySQL database named:CodingChallenge_dev_db
2- add your database credentials in settings.py at line 87,88 ("USER": "your_db_name", "PASSWORD": "your_db_pass")
3- python manage.py migrate. If that doesn't work, do python manage.py migrate shop_workflow
4- python manage.py createsuperuser

5- Loading CSV file would be: python manage.py load_csv
    -this will lookf for a csv file named "seed.csv" inside the data folder

6- Command to run the report (mechanic per repair type) would be: python manage.py gen_reports
    -this will print the report in your shell screen

Assumptions: I considered the column id (in the example table)to be the primary key: In other\ 
words, in the example table given, data from line 4 (Rich) will be \
replaced by data from line 5 (Simone).\If the initial data was not\
mistakenly given, in this case, I will need to change this line\
repair_data,repair_created = CarRepair.objects.get_or_create(id=row.id)\
to this line:
repair_data,repair_created = CarRepair.objects.get_or_create(id=row.id,assigned_mechanic = repair_mechanic)

    -TODO: should change iteration in gen_reports.py to lambda expression
    -Gotcha: There might be a small issue with Rich's record for repair type D. Need to dig in further
