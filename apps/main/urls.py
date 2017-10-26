from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^pokes$', views.pokes),
    url(r'^newpoke$', views.newpoke),
    url(r'^logout$', views.logout),
]
