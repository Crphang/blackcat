from django.conf.urls import patterns, url
from api import views

urlpatterns = patterns(
	'',
	url(r'^$', views.index, name='index'),
	url(r'^event\/get$', views.event_detail, name='event_detail'),
	url(r'^event\/get_events$', views.event_index, name='event_index'),
	url(r'^event\/comment$', views.comment, name='comment'),
	url(r'^event\/like$', views.like, name='like'),
	url(r'^event\/register$', views.register, name='register'),
	url(r'^user\/login$', views.login, name='login'),
	url(r'^user\/logout$', views.logout, name='logout'),
	url(r'^category\/get_categories$', views.categories_index, name='categories_index'),
)
