from person.models import Person
from job.models import Job
from bid.models import Bid
from comment.models import Comment
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, DetailView, ListView
from comment.forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from message.models import Message


class CommentCreateView(CreateView):
	"""docstring for CommentCreateView"""
	model=Comment
	success_url = '/'
	form_class = CommentForm
	
	def get_form_kwargs( self, **kwargs ):
		''' passes the slug of url to the clean of forms in bid 
		'''
		kwargs = super(CommentCreateView, self ).get_form_kwargs(**kwargs)
		kwargs.update({'user': self.request.user,'fuck': self.request.session['job'],})
		return kwargs

	def form_valid(self, form, **kwargs):
		''' Validates the form of Comment 
			also puts the bidder and job 
		'''
		self.object = form.save(commit=False)
		job = self.request.session['job']
		form.instance.job = job
		
		person=Person.objects.get(person=self.request.user)
		form.instance.commentor=person

		profile = person
		profile_class = profile.person_class.person_class
		if profile_class =='doer':
			receiver=job.creator
			
		elif profile_class == 'poster':
			receiver = self.object.receiver

		message = """
			<a href='%s'>%s</a> has reviewed you on task <a href='%s'> %s</a>.
			View your <a href='%s'>profile</a> to see.
				""" % (person.get_absolute_url, person, 
					job.get_absolute_url(), job, receiver.get_absolute_url())
		m = Message(title="Comment", content=message, receiver=receiver, sender=person)
		m.save()
		return super(CommentCreateView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(CommentCreateView,self).get_context_data(**kwargs)
		context['job'] = self.request.session['job']
		return context

	def dispatch(self, request, *args, **kwargs):
		try:
			if not request.user.is_authenticated():
				return HttpResponseRedirect('/login/')
			poster = Person.objects.get(person=self.request.user)
			job = self.request.session['job']
			profile = poster
			profile_class = profile.person_class.person_class
			if profile_class == 'poster':
				if Comment.objects.filter(job=job,commentor=poster).count() == job.number_employee:
					context={'message':'Already commented enough people'}
					return render_to_response('comment/comment_message.html',
		              context,
		              context_instance=RequestContext(request))
			elif profile_class == 'doer':
				if Comment.objects.filter(job=job,commentor=poster):
					context={'message':'Already commented'}
					return render_to_response('comment/comment_message.html',
		              context,
		              context_instance=RequestContext(request))
			return super(CommentCreateView, self).dispatch(request, *args, **kwargs)
		except KeyError, e:
			return HttpResponseRedirect('/')		