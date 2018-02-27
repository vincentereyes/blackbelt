from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index),
	url(r'^main$', views.loginreg),
	url(r'^register$', views.register),
	url(r'^logout$', views.logout),
	url(r'^login$', views.login),
	url(r'^dashboard$', views.dashboard),
	url(r'^additem$', views.additem),
	url(r'^add$', views.add),
	url(r'^wish_items/(?P<iid>\d+)$', views.showitem),
	url(r'^add/(?P<iid>\d+)$', views.addwish),
	url(r'^delete/(?P<iid>\d+)$', views.delete),
	url(r'^remove/(?P<iid>\d+)$', views.remove)
]