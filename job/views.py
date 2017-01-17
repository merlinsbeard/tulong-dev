from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django import forms
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, ListView
from job.forms import JobPostForm, JobComment
from person.models import Person, PersonClassification
from datetime import datetime
from job.models import *
from message.models import Message
from bid.forms import BidForm
from bid.models import Bid
from comment.models import Comment

class RemoveJob(DeleteView):
	'''
	removes job 
	'''
	model = Job
	success_url = '/'
	template_name = 'job_confirm_delete.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		person = Person.objects.get(person=self.request.user)
		job = Job.objects.get(slug=kwargs['slug'])
		if job.creator == person:
			return super(RemoveJob, self).dispatch(*args, **kwargs)
		else:
			return HttpResponseForbidden('forbidden')

class JobCreate(CreateView):
	"""
		Posters can create Job Posts
	"""
	form_class = JobPostForm
	template_name = 'job_create.html'

	@method_decorator(login_required(redirect_field_name='/job/post/'))
	def dispatch(self, *args, **kwargs):
		profile = Person.objects.get(person=self.request.user)
		profile_class = profile.person_class.person_class
		if profile_class == 'doer':
			return HttpResponseForbidden('forbidden')
		return super(JobCreate, self).dispatch(*args, **kwargs)

	def form_valid(self, form):
		poster = Person.objects.get(person=self.request.user)
		form.instance.creator = poster
		return super(JobCreate, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(JobCreate, self).get_context_data(**kwargs)
		
		return context

class JobList(ListView):
	"""
	Lists all jobs in all areas and all categories
	"""
	#queryset = Job.objects.filter(date_need__gte=datetime.now())
	paginate_by = 20

	def get_queryset(self):
		"""
		Searches title and content__icontains
		"""
		if 'q' in self.request.GET:
			q = self.request.GET['q']
			queryset = Job.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(city__icontains=q))
		else:
			queryset = Job.objects.all()
			
		return queryset.filter(date_need__gte=datetime.now())

	def get_context_data(self, **kwargs):
		"""
		filters job excludes past jobs
		"""
		context = super(JobList, self).get_context_data(**kwargs)
		jobs = Job.objects.all()
		jobs = jobs.filter(date_need__gte=datetime.now())
		context['antipolo'] = jobs.filter(city="Antipolo City")
		context['marikina'] = jobs.filter(city="Marikina City")
		context['cainta'] = jobs.filter(city="Cainta")
		context['jobs'] = jobs
		context['sticky'] = Job.objects.filter(is_sticky=True)
		context['categories'] = JobType.objects.all()
		try:
			q = self.request.GET['q']
		except:
			q = False
		context['q'] = q
		return context

class JobListAntipolo(ListView):
	#queryset = Job.objects.filter(date_need__gte=datetime.now())
	paginate_by = 20
	template_name = 'area/job_list_antipolo.html'

	def get_queryset(self):
		if 'q' in self.request.GET:
			q = self.request.GET['q']
			queryset = Job.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(city__icontains=q))
		else:
			queryset = Job.objects.all()
		return queryset.filter(date_need__gte=datetime.now(), city="Antipolo City")

	def get_context_data(self, **kwargs):
		context = super(JobListAntipolo, self).get_context_data(**kwargs)
		jobs = Job.objects.all()
		jobs = jobs.filter(date_need__gte=datetime.now())
		context['antipolo'] = jobs.filter(city="Antipolo City")
		context['marikina'] = jobs.filter(city="Marikina City")
		context['cainta'] = jobs.filter(city="Cainta")
		context['jobs'] = jobs
		context['sticky'] = Job.objects.filter(is_sticky=True)
		try:
			q = self.request.GET['q']
		except:
			q = False
		context['q'] = q
		return context

class JobListMarikina(ListView):
	paginate_by = 20
	template_name = 'area/job_list_marikina.html'

	def get_queryset(self):
		if 'q' in self.request.GET:
			q = self.request.GET['q']
			queryset = Job.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(city__icontains=q))
		else:
			queryset = Job.objects.all()
		return queryset.filter(date_need__gte=datetime.now(), city="Marikina City")

	def get_context_data(self, **kwargs):
		context = super(JobListMarikina, self).get_context_data(**kwargs)
		jobs = Job.objects.all()
		jobs = jobs.filter(date_need__gte=datetime.now())
		context['antipolo'] = jobs.filter(city="Antipolo City")
		context['marikina'] = jobs.filter(city="Marikina City")
		context['cainta'] = jobs.filter(city="Cainta")
		context['jobs'] = jobs
		context['sticky'] = Job.objects.filter(is_sticky=True)
		try:
			q = self.request.GET['q']
		except:
			q = False
		context['q'] = q
		return context

class JobListCainta(ListView):
	paginate_by = 20
	template_name = 'area/job_list_cainta.html'

	def get_queryset(self):
		if 'q' in self.request.GET:
			q = self.request.GET['q']
			queryset = Job.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(city__icontains=q))
		else:
			queryset = Job.objects.all()
		return queryset.filter(date_need__gte=datetime.now(), city="Cainta")

	def get_context_data(self, **kwargs):
		context = super(JobListCainta, self).get_context_data(**kwargs)
		jobs = Job.objects.all()
		jobs = jobs.filter(date_need__gte=datetime.now())
		context['antipolo'] = jobs.filter(city="Antipolo City")
		context['marikina'] = jobs.filter(city="Marikina City")
		context['cainta'] = jobs.filter(city="Cainta")
		context['jobs'] = jobs
		context['sticky'] = Job.objects.filter(is_sticky=True)
		try:
			q = self.request.GET['q']
		except:
			q = False
		context['q'] = q
		return context


class JobBidDetail(DetailView):
	"""Contains the details of JOB"""
	model = Job
	
	def get_context_data(self,**kwargs):

		'''
		public - can view job description and kaakays who bid
		kaakays - same as above but can bid
		winners - same as above plus see secret details
		poster  - view all plus those who bids
		'''
		context	= {}
		winners	= []
		bidders	= []
		job 	= self.object
		employee_need = job.number_employee
		bid_chosen 	  = job.bid_set.filter(is_chosen=True)
		for bid in bid_chosen:
			winners.append(bid.bidder)
		context['bid_winners'] = winners

		# authenticated users
		if self.request.user.is_authenticated():
			profile = Person.objects.get(person=self.request.user)
			profile_class = profile.person_class.person_class

			if job.creator == profile or profile.person.is_staff==True:
				context['is_creator'] = True
				context['view_secret'] = True
				if job.is_done:
					if job.comment_set.filter(commentor=profile).count() >= employee_need:
						context['is_done_comment'] = True

			if profile in winners:
				context['is_winner'] = True
				context['view_secret'] = True
				if job.is_done:
					if job.comment_set.filter(commentor=profile).count() >= 1:
						context['is_done_comment'] = True

			if profile_class == 'doer':
				context['is_doer'] = True

				for bid in job.bid_set.all():
					bidders.append(bid.bidder)
				if profile in bidders:
					context['done_bidding'] = True
					context['doer_bid'] = job.bid_set.get(bidder=profile)

		else: # Public profile
			context['is_public'] = True
		if job.date_need.date() < datetime.now().date():
			context['job_expired']=True

		if bid_chosen.count() >= employee_need:
			context['has_winners'] = True

		elif bid_chosen.count() < employee_need:
			context['incomplete_winners'] = True

		return super(JobBidDetail, self).get_context_data(**context)


	def post(self, request, *args, **kwargs):
		"""
		Button for adding new BIDDING, COMMENTING, and DISCUSSION.
		gets session of job to be passed to bid, comment, or discusion application
		"""
		job = Job.objects.get(slug=kwargs['slug'])
		request.session['job']=job
		job_sample=request.session['job']
		context={'status':job_sample}

		if 'bid' in request.POST:
			return HttpResponseRedirect('/bid/add/')
		elif 'comment' in request.POST:
			return HttpResponseRedirect('/comment/post/')
		elif 'discussion' in request.POST:
			return HttpResponseRedirect('/discussion/add/')
		else:
			return HttpResponseRedirect('/')

def removeExcessNotification(profile):
	# removes excess notifcation of user maximum of 10 notifications
	mes = Message.objects.filter(receiver=profile)[10:]
	mes = Message.objects.filter(id__in=mes).delete()

@login_required	
def updateJob(request, slug):
	#Updates the Job if its done already
	#The Chosen Kaakay are the one who can Update the Job/task

	profile = Person.objects.get(person=request.user)
	job = Job.objects.get(slug=slug)
	bid_winners_id=[]

	#if profile != job.creator:
	#	return HttpResponseRedirect('/')
	if not job.has_winner or job.is_done:
		return HttpResponseForbidden('forbidden')

	for bid in job.bid_set.filter(is_chosen=True):
		bid_winners_id.append(bid.bidder.id)
	winners = Person.objects.filter(id__in=bid_winners_id)

	if profile not in winners:
		return HttpResponseForbidden('you are not allowed here') 

	if request.method == 'POST':
		if job.is_done:
			return HttpResponseForbidden('Job already done')

		if 'yes' in request.POST:
			winners = []
			job.is_done	= True
			post_a_job 	= reverse
			status 	= """
				Job is done! Post another task? 
				Don't forget to give out comments and ratings to kaakays
						"""
			context = {
					'status': status,
					'back' : job.get_absolute_url(),
							}
			job.save()
			
			#Sends a message and email to both Kaakays and Posters
			subject = "%s task is Done!" % (job.title)
			message = """
				<a href='%s'>%s</a> has confirmed <a href='%s'>%s</a> 
				task is done!.
					""" % (profile.get_absolute_url(), profile.firstname, 
						job.get_absolute_url(), job.title)

			#Send email to Bid Winners
			for bid in job.bid_set.filter(is_chosen=True):
				winners.append(bid.bidder.person.email)

			email_content = render_to_string('email/job_done_kaakay.html',)
			send_mail(subject,email_content,'support@tulong.ph',winners)

			# send notification message to all winners of bid
			for bid in job.bid_set.filter(is_chosen=True):
				m=Message(title=subject, content=message, receiver=bid.bidder, sender=profile)
				removeExcessNotification(bid.bidder)
				m.save()

			# send message notification to Job Poster
			subject = "%s task is done." % (job.title)
			message = """
				<a href='%s'>%s</a> has confirmed task <a href='%s'>%s</a> is done.
				<a href='%s'>View</a> to Give comment and Rating.
				""" % (profile.get_absolute_url(), profile, job.get_absolute_url(),
						job, job.get_absolute_url())
			m = Message(title=subject,content=message, receiver=job.creator, sender=profile)
			removeExcessNotification(job.creator)
			m.save()
			
			#Send Email to Job Poster
			email_content = render_to_string('email/job_done_poster.html')
			send_mail(subject,email_content,'support@tulong.ph',[job.creator.person.email], fail_silently=False)

			return render_to_response('success.html',
			              context,
			              context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/')
	else:
		context= {'hello':'hello'}
		return render_to_response('job/job_confirm_done.html',
		              context,
		              context_instance=RequestContext(request))



@login_required
def allBids(request, slug):
	profile = Person.objects.get(person=request.user)
	profile_class = profile.person_class.person_class

	if profile_class == 'poster':
		job = Job.objects.get(slug=slug)
		if profile == job.creator:
			
			context={'job':job}
			return render_to_response('job_all_bids.html',
				              context,
				              context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')

def jobCat(request, slug):
	job_type = JobType.objects.get(slug=slug)
	job_types = JobType.objects.all()
	job_list = Job.objects.filter(job_type=job_type)
	sticky = Job.objects.filter(is_sticky=True)

	if 'q' in request.GET:
		q = request.GET['q']
		queryset = job_list.filter(Q(title__icontains=q) |
							 Q(content__icontains=q) | 
							 Q(city__icontains=q))
	else:
		queryset = job_list
		q = False
	context={
		'job_list':queryset, 'job_type':job_type, 
		'categories':job_types, 'q': q,
		'sticky': sticky
			}
	return render_to_response('job_all_cat.html',
								context,
								context_instance=RequestContext(request))