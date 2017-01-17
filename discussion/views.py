from django.views.generic import CreateView
from discussion.models import Discussion
from person.models import Person
from job.models import Job 
from discussion.forms import DiscussionForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.utils.decorators import method_decorator
from message.models import Message

class AddDiscussion(CreateView):
	model = Discussion 
	form_class = DiscussionForm

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		if not self.request.session['job']:
			return HttpResponseRedirect('/')
		return super(AddDiscussion, self).dispatch(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(AddDiscussion, self).get_context_data(**kwargs)
		context['job'] = self.request.session['job']
		return context

	def form_valid(self, form, **kwargs):
		job = self.request.session['job']
		profile = Person.objects.get(person=self.request.user)
		form.instance.job = job
		form.instance.person = profile
		ids = []
		for d in job.discussion_set.all():
			if d.person != profile:
				ids.append(d.person.id)
		receiver = Person.objects.filter(id__in=ids)
		for person in receiver:
			message = """
				<a href='%s'>%s</a> has a comment on task <a href='%s'> %s</a>
					""" % (profile.get_absolute_url(), profile,
					 job.get_absolute_url(),job )
			m = Message(title="Comment", content=message, receiver=person, sender=profile)
			m.save()
		return super(AddDiscussion, self).form_valid(form)

	def get_success_url(self, **kwargs):
		job = self.request.session['job']
		url = job.get_absolute_url()
		return url