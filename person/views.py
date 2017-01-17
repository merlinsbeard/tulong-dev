from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from person.models import Person, PersonClassification
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from person.models import Person
from job.models import Job
from bid.models import Bid
from django.views.generic import TemplateView, DetailView, ListView, UpdateView
from message.models import Message
from comment.models import Comment
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from person.forms import UpdateInform


class PersonUpdate(UpdateView):
        model = Person
        template = 'person/person_form_update.html'
        form_class = UpdateInform

        @method_decorator(login_required)
        def dispatch(self, *args, **kwargs):
                person = self.request.user
                if person.is_staff:
                        return super(PersonUpdate, self).dispatch(*args, **kwargs)
                else:
                        return HttpResponseForbidden('forbidden')
        def get_context_data(self, *args, **kwargs):
                context = super(PersonUpdate, self).get_context_data(**kwargs)
                if self.request.user.is_staff:
                        context['is_staff'] = True
                return context

class PersonList(ListView):
        model = Person
        doer = PersonClassification.objects.get(person_class='doer')
        queryset = Person.objects.filter(is_verified=True, person_class=doer)
class PersonKaakayList(ListView):
	model 	 = Person
        doer = PersonClassification.objects.get(person_class='doer')
        queryset = Person.objects.filter(is_verified=True, person_class=doer)	

class PersonDetail(DetailView):
        model = Person

        def post(self, request, *args, **kwargs):
                """
                Button for adding new BIDDING, COMMENTING, and DISCUSSION.
                gets session of job to be passed to bid, comment, or discusion application
                """
                
                profile = Person.objects.get(person=request.user)
                kaakay = Person.objects.get(slug=kwargs['slug'])
                request.session['kaakay']=kaakay
                
                context={'status':request.session['kaakay']}
                kaakay = self.request.session['kaakay']
                poster = Person.objects.get(person=self.request.user)
                message = "<a href='%s'>%s</a> wants you for task" % (poster.get_absolute_url(), poster)
                m=Message(title="Poster wants you!", content=message, receiver=kaakay, sender=profile)
                m.save()
                return HttpResponseRedirect('/job/post')

        def get_context_data(self, **kwargs):

                person = kwargs['object']
                context={'person':person,}
                comments = person.receiver.all()
                profile = person
                profile_class = profile.person_class.person_class
                if self.request.user.is_authenticated():
                        poster = Person.objects.get(person=self.request.user)
                        profile_class = poster.person_class.person_class
                        if profile_class == 'poster': 
                                context['is_poster']=True
                if comments:
                        total = 0
                        for c in comments:
                                total = total + c.rating
                        rating_average = total/comments.count()
                        context['comments'] = comments[:5]
                        context['rating']  = rating_average
                if profile_class == 'poster':
                        context['person_poster']=True
                        context['jobs_done'] = Job.objects.filter(is_done=True, creator=person)
                        context['jobs'] = Job.objects.filter(creator=person)
                elif profile_class == 'doer':
                        bids = Bid.objects.filter(bidder=person, is_chosen=True)
                        context['person_doer']  = True
                        context['bids']         = bids
                        list_of_pk              = []
                        for bid in Bid.objects.filter(bidder=person, is_chosen=False):
                                if bid.job.is_done == False:
                                        list_of_pk.append(bid.pk)
                        context['pending_bids'] = Bid.objects.filter(pk__in=list_of_pk)
                        jobs=[]
                        for b in bids:
                                jobs.append(b.job.id)
                        context['jobs'] = Job.objects.filter(is_done=True, id__in=jobs)
                return super(PersonDetail, self).get_context_data(**context)


def allComments(request, slug):
        profile = Person.objects.get(slug=slug)
        comments = Comment.objects.filter(receiver=profile)
        context={'profile':profile, 'comments':comments,}
        return render_to_response('person/person_comment_all.html', context, 
                context_instance=RequestContext(request))
