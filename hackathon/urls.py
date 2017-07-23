from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', views.org_view, name='org_view'),
	url(r'^dataElements/', views.data_elements_view, name='data_view'),
	url(r'^geodata/', views.org_map_data, name='gis_data'),
	url(r'^geodata4/', views.get_g_4, name='gis_data_4'),
	url(r'^map/', views.map_view, name='org_map'),
	url(r'^analytics/', views.analytics, name='analytics'),
	url(r'^graphs/', views.graphs, name='graphs'),
	url(r'^analytics_data/', views.analytics_data, name='analytics_data'),
]
