from django.conf.urls import patterns, include, url


import views
urlpatterns = patterns('',
   
    url(r'^$', views.PersonList.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', views.PersonDetail.as_view(), name="detail"),
    url(r'^(?P<slug>[\w-]+)/comments/$','person.views.allComments', name="comments'"),
    url(r'^(?P<slug>[\w-]+)/update/$',views.PersonUpdate.as_view(), name="update'"),


)
