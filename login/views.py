from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from login.forms import LoginForm
from django.contrib.auth.models import User
from person.models import Person, PersonClassification
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from register.forms import RegistrationForm
from register.views import PersonRegistration

def LoginRequest(request):
        if request.user.is_authenticated():
                return HttpResponseRedirect('/dashboard/')
        if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']
                        person = authenticate(username=username, password=password)
                        if person is not None:
                                if person.person.is_verified == True:
                                        login(request, person)
                                        return HttpResponseRedirect('/login/?next=%s' % request.path)
                                        #return HttpResponseRedirect('/dashboard/')
                                else:
                                        return render_to_response('not_verified.html', {'status': 'You are not yet verified'}, context_instance=RequestContext(request))
                               # login(request, person)
                               # return HttpResponseRedirect('/login/?next=%s' % request.path) 
                                
                        else:
                                return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
                else:
                        return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
        else:
                ''' user is not submitting the form, show the login form '''
                form = LoginForm()
                context = {'form': form}
                return render_to_response('login.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
        logout(request)
        return HttpResponseRedirect('/')

def mix_of_login_register(request, slug):
        """
        Template contains 2 forms, the login and the registration
        """
        if slug == 'doer':
                is_doer = True
                is_poster = False
        elif slug == 'poster':
                is_poster = True
                is_doer = False
        if request.user.is_authenticated():
                return HttpResponseRedirect('/dashboard/')
	if 'login' in request.POST:
		return LoginRequest(request)
        elif 'register' in request.POST:
                return PersonRegistration(request, slug)
        else:
                form = LoginForm()
                form2 = RegistrationForm()
                context = {'form':form, 'form2': form2, 'is_doer': is_doer, 'is_poster': is_poster,}
                return render_to_response('mixlogin.html', context, context_instance=RequestContext(request))

