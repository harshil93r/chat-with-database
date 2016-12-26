from django.conf.urls import url
from . import views

urlpatterns = [
    # /dashboards/
    url(r'^$', views.dashboard),
    # /dashboards/1/
    # url(r'^(?P<dash_id>[0-9]+)/$', views.dash),
    
]