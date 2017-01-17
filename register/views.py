from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from register.forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User
from person.models import Person, PersonClassification
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.conf import settings

class RegisterChoose(TemplateView):
        template_name = 'register/register_option.html'
        
def PersonRegistration(request, slug):

        if slug == 'doer':
                is_doer = True
                is_poster = False
        elif slug == 'poster':
                is_poster = True
                is_doer = False

        if request.user.is_authenticated():
                return HttpResponseRedirect('/profile/')
        if request.method == 'POST':
                form = RegistrationForm(request.POST)
                if form.is_valid():
                        user = User.objects.create_user(
                                username  = form.cleaned_data['email'],
                                email     = form.cleaned_data['email'],
                                password  = form.cleaned_data['password'],
                                )
                        firstname = form.cleaned_data['firstname']
                        lastname  = form.cleaned_data['lastname']
                        user.first_name = firstname
                        user.last_name  = lastname
                        name = '%s %s' % (user.first_name , user.last_name)
                        p = PersonClassification.objects.get(slug=slug)
                        a = slug
                        slug = str(user.id) + str(datetime.now().day) + str(datetime.now().year)
                        skills = form.cleaned_data['skills']
                        person = Person(
                                person         = user,
                                person_class   = p,
                                is_verified    = False,
                                is_active      = False,
                                address        = form.cleaned_data['address'],
                                birthday       = form.cleaned_data['birthday'],
                                firstname      = form.cleaned_data['firstname'],
                                lastname       = form.cleaned_data['lastname'],
                                created_at     = datetime.now(),
                                contactno      = form.cleaned_data['contactno'],
                                #classification = a,
                                )

                        user.save()
                        person.save()
                        person.skills=skills
                        if person.person_class.__str__() == 'poster':
                                template = 'register_poster.html'
                        else:
                                template = 'register_doer.html'

                        
                        '''
                        send verification instructions to user
                        '''
                        subject='Welcome to Tulong.ph' 
                        message='Hi %s we from tulong.ph, gladly welcomes you. Please reply to this email if you have any questions.' % person.firstname
                        to = person.person.email
                        #send_mail(subject,message,'support@tulong.ph',[to],fail_silently=False)
                        
                        name = "%s %s" % (person.firstname, person.lastname )
                        context = { 'full_name': name, 'person':person }
                        text_content = render_to_string('email/register.html', context)
                        html_content = render_to_string('email/register_html.html', context)
                        msg = EmailMultiAlternatives(subject, text_content,
                                                settings.EMAIL_HOST_USER, [to])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                        #send_mail(subject, email_content, 
                        #        settings.EMAIL_HOST_USER, [to],fail_silently=False)
                        '''
                        send the new user to the admin 
                        '''
                        person_classification = person.person_class.__str__()
                        subject='New User as %s' % (person_classification)
                        message='User %s Registered as %s ' % (person.person.email, person_classification)
                        to = 'tulongph@outlook.com'
                        send_mail(subject,message,'support@tulong.ph',[to],fail_silently=False)
                        
                        return render_to_response(template, 
                                {
                                'status': person, 'is_doer': is_doer, 
                                'is_poster': is_poster,
                                }, 
                                context_instance=RequestContext(request))
                        #return HttpResponseRedirect('/login/')
                else:
                        return render_to_response(
                                        'register.html', 
                                        {'form': form, 'is_doer': is_doer, 
                                        'is_poster': is_poster,},
                                         context_instance=RequestContext(request)
                                                )

        else:
                ''' user is not submitting the form, show them a blank registration form '''
                form = RegistrationForm()
                context = {'form': form, 'is_doer': is_doer, 'is_poster': is_poster,}
                return render_to_response('register.html', 
                                context, context_instance=RequestContext(request))
		


def LogoutRequest(request):
        logout(request)
        return HttpResponseRedirect('/')

def registration(request):
        if request.user.is_authenticated():
                return HttpResponseRedirect('/profile/')
        if request.method == 'POST':
                form = RegistrationForm(request.POST)
                if form.is_valid():
                        user = User.objects.create_user(
                                username  = form.cleaned_data['email'],
                                email     = form.cleaned_data['email'],
                                password  = form.cleaned_data['password'],
                                )
                        firstname = form.cleaned_data['firstname']
                        lastname  = form.cleaned_data['lastname']
                        user.first_name = firstname
                        user.last_name  = lastname
                        name = '%s %s' % (user.first_name , user.last_name)
                        
                        a=request.session['classification']
                        p = PersonClassification.objects.get(slug=a)
                        slug = str(user.id) + str(datetime.now().day) + str(datetime.now().year)
                        skills  =form.cleaned_data['skills'],
                        person = Person(
                                person         = user,
                                person_class   = p,
                                is_verified    = False,
                                is_active      = False,
                                address        = form.cleaned_data['address'],
                                birthday       = form.cleaned_data['birthday'],
                                firstname      = form.cleaned_data['firstname'],
                                lastname       = form.cleaned_data['lastname'],
                                created_at     = datetime.now(),
                                contactno      = form.cleaned_data['contactno'],
                                classification = a,
                                )

                        user.save()
                        person.save()
                        person.skills=skills
                        if a == 'poster':
                                template = 'register_poster.html'
                        else:
                                template = 'register_doer.html'

                        '''
                        send verification instructions to user
                        '''
                        subject='Welcome to Tulong.ph' 
                        message='Hi %s we from tulong.ph, gladly welcomes you. Please reply to this email if you have any questions.' % person.firstname
                        to = person.person.email
                        email_from = 'support@tulong.ph'
                        send_mail(subject,message,email_from,[to],fail_silently=False)
                        '''
                        send the new user to the admin 
                        '''
                        subject='new user'
                        message='user %s registered' % person.firstname
                        to = email_from
                        send_mail(subject,message,email_from,[to],fail_silently=False)

                        return render_to_response(template, {'status': person}, context_instance=RequestContext(request))
                        
                else:
                        return render_to_response('register.html', {'form': form,'test':request.session['classification'],}, context_instance=RequestContext(request))

        else:
                ''' user is not submitting the form, show them a blank registration form '''
                form = RegistrationForm()
                context = {'form': form,'test':request.session['classification'],}
                return render_to_response('register.html', context, context_instance=RequestContext(request))
