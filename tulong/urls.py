from django.conf.urls import patterns, include, url
#from django.contrib.auth.views import password_reset

from django.contrib import admin
admin.autodiscover()
import views
urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^register/',include('register.urls', namespace="register")),

	url(r'^person/',include('person.urls', namespace="person")),   
    url(r'^login/$', 'login.views.LoginRequest', name="login"),
    url(r'^logout/$', 'login.views.LogoutRequest', name="logout"),
    url(r'^loginregister/$', 'login.views.mix_of_login_register'),

    url(r'^$', views.HomepageView.as_view(), name="home"),
    url(r'^otherhome$', views.OtherHomepageView.as_view(),),
    url(r'^contactus/$', views.contactus, name="contact"),
    #url(r'^$','contactus.views.contactus'),
    url(r'^aboutus/$', views.AboutUs.as_view(), name="aboutus"),
    url(r'^aboutus/faqs/$', views.FAQS.as_view(), name="faqs"),
    url(r'^terms/$', views.Terms.as_view(), name="terms_and_conditions"),


    url(r'^job/', include('job.urls', namespace="job")),
    url(r'^bid/',include('bid.urls', namespace="bid")),
    
    #url(r'^person/',include('person.urls', namespace="person")),
    url(r'^message/',include('message.urls', namespace="message")),

    (r'^ckeditor/', include('ckeditor.urls')),

    url(r'^comment/',include('comment.urls', namespace="comment")),

    url(r'^discussion/',include('discussion.urls', namespace="discussion")),

    url(r'^dashboard/',include('dashboard.urls', namespace="dashboard")),
    
    #url('^markdown/', include( 'django_markdown.urls')),


    (r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
)
