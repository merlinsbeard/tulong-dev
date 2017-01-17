from django.conf.urls import patterns, include, url


import views
urlpatterns = patterns('',
    url(r'^$', views.MessageList.as_view(), name='list'),
    url(r'^list/(?P<slug>[\w-]+)/$', views.MessageDetail.as_view(), name="detail"),
)
