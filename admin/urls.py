from django.conf.urls import patterns, url
from admin import views

urlpatterns = patterns(
	'',
	url(r'^$', views.index, name="index"),
	url(r'^upload$', views.image_upload, name='upload'),
	url(r'^create_event$', views.create_event, name='create_event'),
	url(r'^create_category$', views.create_category, name='create_category'),
	url(r'^create_event_category$', views.create_event_category, name='create_event_category')
)
