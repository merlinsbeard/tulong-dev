from django.conf.urls import patterns, include, url



import views

urlpatterns = patterns('',
   
    url(r'^post/', views.JobCreate.as_view(), name="post"),
    url(r'^$', views.JobList.as_view(), name="list"),
    #url(r'^area/$', views.JobListSearch.as_view(), name="area"),
    url(r'^antipolo/$', views.JobListAntipolo.as_view(), name="antipolo"),
    url(r'^marikina/$', views.JobListMarikina.as_view(), name="marikina"),
    url(r'^cainta/$', views.JobListCainta.as_view(), name="cainta"),
    url(r'^all/$', views.JobList.as_view(), name="all"),
    url(r'^all/(?P<slug>[\w-]+)$', 'job.views.jobCat', name="cat"),

    #url(r'^$', 'job.views.jobList', name="list"),
	url(r'^list/(?P<slug>[\w-]+)/$', views.JobBidDetail.as_view(), name="detail"),
	url(r'^list/(?P<slug>[\w-]+)/delete/$', views.RemoveJob.as_view(), name="delete"),
	url(r'^list/(?P<slug>[\w-]+)/done/$', 'job.views.updateJob', name="done"),
	url(r'^list/(?P<slug>[\w-]+)/allbids/$', 'job.views.allBids', name="allbids"),
	
)
