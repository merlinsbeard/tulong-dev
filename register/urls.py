from django.conf.urls import patterns, include, url
import views
urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)/$', 'login.views.mix_of_login_register', name="register"),
   #url(r'^$', 'register.views.registration', name="solo"),
    url(r'^$', views.RegisterChoose.as_view(), name="reg"),

)
