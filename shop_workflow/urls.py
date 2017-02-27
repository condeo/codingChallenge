from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /shop_workflow/
    #url(r'^$', views.index, name='index'),
    # ex: /mechanic_infos/5/
    #url(r'^(?P<mechanic_infos>[0-9]+)/$', views.mechanic_infos, name='mechanic_infos'),
    # ex: /repair_details/5/
    #url(r'^(?P<repair>[0-9]+)/$', views.repair_details, name='repair_details'),
    # ex: shop_workflow/repairs/
    url(r'^/repairs/$', views.repairs, name='repairs'),
    # ex: /job/5/mechanics/
    #url(r'^(?P<job_type>[0-9]+)/mechanics/$', views.rank_per_job_type, name='rank_per_job_type'),
]