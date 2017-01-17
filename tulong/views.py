from django.views.generic import TemplateView
from django.contrib.auth.models import User
from person.models import PersonClassification, Person
from django.http import HttpResponseRedirect
from tulong.forms import ContactForm

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

from twilio.rest import TwilioRestClient
import datetime
from datetime import date

from django.conf import settings


class HomepageView(TemplateView):
	template_name = "index.html"

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect('/dashboard/')
		return super(HomepageView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(HomepageView,self).get_context_data(**kwargs)
		context['classifications'] = PersonClassification.objects.all()
		return context
	
	def post(self, request, *args, **kwargs):
		if 'doer' in request.POST:
			classification='doer'
		elif 'poster' in request.POST:
			classification='poster'
		else:
			return HttpResponseRedirect('/')
		request.session['classification']=classification
		return HttpResponseRedirect('/register/')

class ContactUs(TemplateView):
	template_name = "contactus.html"

def send_text_message(to, message):
	account_sid = settings.TWILIO_ACCOUNT_SID
	auth_token = settings.TWILIO_AUTH_TOKEN
	from_ = settings.TWILIO_FROM_
	client = TwilioRestClient(account_sid,
							auth_token)
	message = client.sms.messages.create(to=to, 
							from_=from_, body=message)

def send_email_notify(subject, to, dict_context, template):
	context = dict_context
	text_content = render_to_string(template, context)
	html_content = render_to_string(template, context)
	msg = EmailMultiAlternatives(subject, text_content,
	                        settings.EMAIL_HOST_USER, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()

def contactus(request):
	context = {}
	if request.method == 'POST':
		form = ContactForm(request.POST)

		if form.is_valid():
			name = form.cleaned_data['name']
			from_email = form.cleaned_data['email']
			#mobile_number = form.cleaned_data['mobile_number']
			message = form.cleaned_data['message']
			
			
			#mobile_number = '+63' + mobile_number
			
			#text_message = "Contact by %s" % (name[0])
			text_message = "Check your Contact"

			Email = "%s -- %s -- %s" \
				% (name, from_email, message)
			
			success_message = "Congratulations! you have succesfully sent me a message"

			context['name'] = name
			context['from_email'] = from_email 
			#context['mobile_number'] = mobile_number
			context['message'] = message
			

			
			context['success_message'] = success_message

			send_text_message('+639179071139', text_message)
			send_email_notify('New Contact Us','bjpaat01@gmail.com',
								context, 'email/contactus_email_admin.html')
			send_email_notify('Thank you for your message.',from_email,
								context, 'email/contactus_email.html')

			form = ContactForm()
	else:
		form = ContactForm()

	context['form'] = form

	return render_to_response('contactus.html', context,
		RequestContext(request))


class AboutUs(TemplateView):
	template_name = "flats/aboutus.html"

class FAQS(TemplateView):
	template_name = "flats/faqs.html"

class Terms(TemplateView):
	template_name = "flats/terms_and_conditions.html"

class OtherHomepageView(TemplateView):
	template_name = "index2.html"

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect('/dashboard/')
		return super(OtherHomepageView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(OtherHomepageView,self).get_context_data(**kwargs)
		context['classifications'] = PersonClassification.objects.all()
		return context
	
	def post(self, request, *args, **kwargs):
		if 'doer' in request.POST:
			classification='doer'
		elif 'poster' in request.POST:
			classification='poster'
		else:
			return HttpResponseRedirect('/')
		request.session['classification']=classification
		return HttpResponseRedirect('/register/')