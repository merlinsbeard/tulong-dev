from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from bid.models import Bid
from job.models import Job
from person.models import Person
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from person.models import PersonClassification
from django.views.generic import DeleteView, CreateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from message.models import Message
from .forms import BidForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime

class AddBid(CreateView):
	"""
	Add Bid to Job.
	"""
	model = Bid
	success_url = '/'
	form_class = BidForm

	def get_context_data(self,**kwargs):
		context = super(AddBid,self).get_context_data(**kwargs)
		context['bid'] = Bid.objects.all()
		context['job'] = self.request.session['job']
		return context

	def get_form_kwargs( self, **kwargs ):
		''' passes the slug of url to the clean of forms in bid 
		'''
		kwargs = super(AddBid, self ).get_form_kwargs(**kwargs)
		kwargs.update({'user': self.request.user,
						'fuck': self.request.session['job'],})
		return kwargs

	def form_valid(self, form, **kwargs):
		''' Validates the form of bid 
			also puts the bidder and job 
		'''
		job = self.request.session['job']
		profile = Person.objects.get(person=self.request.user)
		receiver = job.creator
		form.instance.bidder = profile
		form.instance.job = job
		name = '%s %s' % (profile.firstname, profile.lastname)
		title = """
					<a href='%s'>%s</a> bid on task <a href='%s'>%s</a>
				""" % (receiver.get_absolute_url(), 
					receiver, job.get_absolute_url,job)
		message = """
			<a href='%s'>%s</a> has bid %s Hire him now or wait for others <a href='%s'>%s</a>
			"""	% (profile.get_absolute_url(),
			profile,job,job.get_absolute_url(),job)
		m = Message(title="New Bidder", content=message, receiver=receiver, sender=profile)
		m.save()
		subject="%s has bid on your %s" % (profile, job)
		
		to = receiver.person.email

		#name = "%s %s" % (person.firstname, person.lastname )
		context={'profile':Person.objects.get(person=self.request.user), 'job':job}
		email_content = render_to_string('email/bid_new.html',context)
		send_mail(subject,email_content,'support@tulong.ph',[to],fail_silently=False)
		#send_mail(subject,message,'support@tulong.ph',[to],fail_silently=False)
		return super(AddBid, self).form_valid(form)
	
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		try:
			if not request.user.is_authenticated():
				return HttpResponseRedirect('/login/')
			poster = Person.objects.get(person=self.request.user)
			if poster.person_class.slug == 'poster':
				return HttpResponseRedirect('/')
			elif poster.person_class.slug=='doer':
				job = self.request.session['job']

				if Bid.objects.filter(bidder=poster,job=job):
					context={'message': 'You have already Bid!'}
					return render_to_response('bid/bid_create_fail.html',
		              context,
		              context_instance=RequestContext(request))

				if job.number_employee == Bid.objects.filter(is_chosen=True,job=job).count():
					context={'message':'Already has enough Kaakays chosen. Cannot bid anymore'}
					return render_to_response('bid/bid_create_fail.html',
		              context,
		              context_instance=RequestContext(request))
			return super(AddBid, self).dispatch(request, *args, **kwargs)
		except KeyError, e:
			return HttpResponseRedirect('/')
		
class RemoveBid(DeleteView):
	model = Bid
	success_url = '/'
	template_name = 'bid_confirm_delete.html'
	
class BidListView(ListView):
	"""
	Lists all of the Bids
	"""
	model = Bid
	def get_context_data(self, **kwargs):
		context = super(BidListView,self).get_context_data(**kwargs)
		context['bid'] = Bid.objects.all()
		return context

class BidDetail(DetailView):
	"""
	View the Details of bid by Kaakays.
	"""
	model = Bid
	
	def dispatch(self, request, *args, **kwargs):
		"""
		Bids can only be viewed by whomever bids them and also the job creator
		"""
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/login/')
		pk = kwargs['pk']
		bid = Bid.objects.get(pk=pk)
		job = bid.job
		if bid.job.creator.person == request.user or bid.bidder.person == request.user:
			return super(BidDetail, self).dispatch(request, *args, **kwargs)
		else:
			return HttpResponseRedirect('/')

	def get_context_data(self, **kwargs):
		context = super(BidDetail,self).get_context_data(**kwargs)
		context['hi'] = self.object
		context.update(kwargs)
		profile = Person.objects.get(person=self.request.user)
		profile_class = profile.person_class.person_class
		if profile_class == 'poster':
			is_poster=True
		else:
			is_poster=False
		context['person']= profile
		context['is_poster'] = is_poster
		bid = self.object
		job = bid.job
		if job.date_need.date() < datetime.now().date():
			context['job_is_expired'] = True
		testing = bid.job.bid_set.all()
		context['testing'] = testing
		return context

	def post(self, request, *args, **kwargs):
		"""
		Checkes if Bid has already been accepted. Accepts the bid if not.
		If already has enough chosen bids, automataically updates the job.
		"""
		pk = kwargs['pk']
		bid = Bid.objects.get(pk=pk)
		job = bid.job
		context={}
		profile = Person.objects.get(person=self.request.user)
		if 'hire' in request.POST:
			number_of_hired_workers=len(job.bid_set.filter(is_chosen=True))
			#Checks if Job already has enough chosen bids
			if number_of_hired_workers != job.number_employee:
				bid.is_chosen = True
				status = "Hired!"
				receiver = bid.bidder
				job.jobworker_set.create(worker=receiver)
				name = '%s %s' % (profile.firstname, profile.lastname[0])
				message = """
					<a href='%s'> %s</a> has chosen your bid at <a href='%s'> %s</a>
					""" % (profile.get_absolute_url(),
						name, job.get_absolute_url(), job)
				m = Message(title="Chosen Bidder", 
					content=message, receiver=receiver, sender=profile)
				m.save()
				receiver.person.email
				subject="%s has chosen your bid at %s" % (name, job)
				message = "Congrats! please check your home page for further details"
				to = receiver.person.email
				#send_mail(subject,message,'support@tulong.ph',[to],fail_silently=False)
				context={'profile':profile, 'job':job}
				email_content = render_to_string('email/bid_accept.html',context)
				send_mail(subject,email_content,'support@tulong.ph',[to],fail_silently=False)
				#check if already has enough people
				job.save()
				bid.save()
				number_of_hired_workers = len(job.bid_set.filter(is_chosen=True))
				if number_of_hired_workers == job.number_employee:
					job.has_winner = True
					job.save()
			else:
				status = "Already Hired the required people!"
		elif 'unhire' in request.POST:
			bid.is_chosen = False
			job = job
			job.has_winner=False
			status = "Unhired!"
		bid.save()
		context['status'] = status
		context['back'] = job.get_absolute_url()
		return render_to_response('success.html',
		              context,
		              context_instance=RequestContext(request))
		