from django.conf.urls import patterns, include, url



import views

urlpatterns = patterns('',
	url(r'^add/', views.AddDiscussion.as_view(), name="add"),
)
