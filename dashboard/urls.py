from django.conf.urls import patterns, include, url



import views
urlpatterns = patterns('',
    url(r'^$', 'dashboard.views.dashboard'),
    url(r'^messages/$', 'dashboard.views.messages', name="messages"),
    url(r'^pendingtasks/$', 'dashboard.views.pendingTasks', name='pending'),
    url(r'^successfultasks/$', 'dashboard.views.successfulTasks', name='successful'),
    url(r'^failedtasks/$', 'dashboard.views.expiredTasks', name='expired'),
    url(r'^update/$', 'dashboard.views.updateProfile', name='update2'),

)
