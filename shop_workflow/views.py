from django.shortcuts import render
from shop_workflow.models import Mechanic, CarRepair
from datetime import datetime

# python loggins
import logging
today_date = datetime.now().strftime("%m-%d-%Y")
extension = 'log'
writepath = 'logs/views_logs{0}.{1}'.format(today_date, extension)
logger = logging.getLogger('views_logs')
hdlr = logging.FileHandler(writepath)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

# Create your views here.
def repairs(request):
    '''
    displays the list of repairs along with their lenght of service
    '''
    repairs_list = CarRepair.objects.order_by('dropoff_date')
    context = {'repairs_list': repairs_list}
    return render(request, 'shop_workflow/index.html', context)
