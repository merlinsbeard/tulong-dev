from django.conf.urls import patterns, include, url



import views

urlpatterns = patterns('',
	url(r'^(?P<pk>\d+)/$', views.BidDetail.as_view(), name="detail"),
	url(r'^$', views.BidListView.as_view(), name="list"),
	url(r'^(?P<pk>\d+)/delete/$', views.RemoveBid.as_view(), name="delete"),
	url(r'^add/', views.AddBid.as_view(), name="add"),
)
