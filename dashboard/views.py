from django.http import HttpResponseRedirect
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
from person.forms import UpdateInform

def get_job_from_bids(bids):
        job_id = []
        for bid in bids:
                job_id.append(bid.job.id)
        return Job.objects.filter(id__in=job_id)

@login_required
def dashboard(request):
        if not request.user.is_authenticated():
                return HttpResponseRedirect('/')
        user1 = request.user
        profile = Person.objects.get(person=user1)
        profile_class = profile.person_class.person_class
        
        context = {
                'person': profile,
                'status': str(profile.person_class),
                'messages': Message.objects.filter(receiver=profile)[:10]
                }
        if profile_class == "doer":
                bids = Bid.objects.filter(bidder=profile)
                context['bids']         = bids
                context['bids_ongoing'] = Bid.objects.filter(bidder=profile, is_chosen=False)
                

                #getting the jobs of won bids not including both done and not done
                bids_won = bids.filter(is_chosen=True)
                jobs = get_job_from_bids(bids_won)
                context['jobs_won']= jobs[:5]
                #getting the jobs won that has no comment
                jobs = get_job_from_bids(bids_won)
                jobs = jobs.filter(is_done=True)
                jobs_id = []
                for job in jobs:
                        if job.comment_set.filter(commentor=profile).count()<1:
                                jobs_id.append(job.id)
                jobs_no_comment = Job.objects.filter(id__in=jobs_id)
                context['jobs_no_comment'] = jobs_no_comment
                # getting failed jobs
                date_one_day = datetime.now() - timedelta(days=1)
                bids_failed = bids.filter(is_chosen=False)
                jobs = get_job_from_bids(bids_failed)
                jobs = jobs.filter(date_need__lt=datetime.now(), is_done=False)
                context['jobs_failed']= jobs[:5]
                # getting the not chosen bids
                jobs = get_job_from_bids(bids_failed)
                jobs = jobs.filter(is_done=True)
                context['jobs_not_chosen']=jobs[:5]
                #getting pending bids
                bids_current = bids.filter(is_chosen=False)
                jobs = get_job_from_bids(bids_current)
                jobs = jobs.filter(date_need__gt=datetime.now(), is_done=False)
                context['jobs_current']= jobs[:5]
                context['bids_win']     = Bid.objects.filter(bidder=profile, is_chosen=True)
                return render_to_response('dashboard_doer.html', context, context_instance=RequestContext(request))
        elif profile_class == 'poster' :
                context['jobs']            = Job.objects.filter(creator=profile, date_need__gt=datetime.now(), is_done=False)[:5]
                context['jobs_finish']     = Job.objects.filter(creator=profile, is_done=True)[:5]
                context['jobs_not_finish'] = Job.objects.filter(creator=profile, is_done=False, date_need__lt=datetime.now())[:5]

                jobs_fin = Job.objects.filter(creator=profile, is_done=True)
                jobs_without_comment_id = []
                for job in jobs_fin:
                        if job.comment_set.filter(commentor=profile).count()<job.number_employee:
                                jobs_without_comment_id.append(job.id)
                context['jobs_need_comment'] = Job.objects.filter(id__in=jobs_without_comment_id)
        return render_to_response('dashboard_poster.html', context, context_instance=RequestContext(request))


@login_required
def messages(request):
        profile = Person.objects.get(person=request.user)
        context={'messages': Message.objects.filter(receiver=profile)}
        return render_to_response('person/person_messages.html', context, context_instance=RequestContext(request))

@login_required
def archiveJobs(request):
        if not request.user.is_authenticated():
                return HttpResponseRedirect('/')
        user1 = request.user
        profile = Person.objects.get(person=user1)
        profile_class = profile.person_class.person_class
        
        context = {
                'person': profile,
                'status': str(profile.person_class),
                }

        if profile_class == 'doer':
                bids                    = Bid.objects.filter(bidder=profile)
                context['bids']         = bids
                context['bids_ongoing'] = Bid.objects.filter(bidder=profile, is_chosen=False)
                context['bids_win']     = Bid.objects.filter(bidder=profile, is_chosen=True)
                
                return render_to_response('dashboard_doer.html', context, context_instance=RequestContext(request))
        elif profile_class == 'poster':
                context['jobs']            = Job.objects.filter(creator=profile)
                context['jobs_finish']     = Job.objects.filter(creator=profile, is_done=True)
                context['jobs_not_finish'] = Job.objects.filter(creator=profile, is_done=False)

        return render_to_response('dashboard_poster.html', context, context_instance=RequestContext(request))

@login_required
def expiredTasks(request):
        profile = Person.objects.get(person=request.user)
        profile_class = profile.person_class.person_class
        context={}
        if profile_class == "doer":
                bids = Bid.objects.filter(bidder=profile)
                context['bids']         = bids
                context['bids_ongoing'] = Bid.objects.filter(bidder=profile, is_chosen=False)
                context['bids_win']     = Bid.objects.filter(bidder=profile, is_chosen=True)
                return render_to_response('person/person_doer_jobs.html', context, context_instance=RequestContext(request))
        elif profile_class == 'poster' :
                context['jobs_status'] = "Expired Tasks"
                context['jobs'] = Job.objects.filter(creator=profile, is_done=False, date_need__lt=datetime.now())
        return render_to_response('person/person_poster_jobs.html', context, context_instance=RequestContext(request))

@login_required
def pendingTasks(request):
        profile = Person.objects.get(person=request.user)
        profile_class = profile.person_class.person_class
        context={}
        if profile_class == "doer":
                bids = Bid.objects.filter(bidder=profile)
                bids_current = bids.filter(is_chosen=False)
                jobs = get_job_from_bids(bids_current)
                jobs = jobs.filter(is_done=False, date_need__gt=datetime.now())
                context['jobs_status'] = "Pending Bids"
                context['jobs']=jobs
                template = 'person/person_doer_jobs.html'
        elif profile_class == 'poster' :
                context['jobs_status'] = "Pending Tasks"
                context['jobs'] = Job.objects.filter(creator=profile, date_need__gt=datetime.now(), is_done=False)
                template = 'person/person_poster_jobs.html'
        return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def successfulTasks(request):
        profile = Person.objects.get(person=request.user)
        profile_class = profile.person_class.person_class
        context={}
        if profile_class == "doer":
                bids = Bid.objects.filter(bidder=profile)
                bids_won = bids.filter(is_chosen=True)
                jobs = get_job_from_bids(bids_won)
                context['jobs']= jobs
                return render_to_response('person/person_doer_jobs.html', context, context_instance=RequestContext(request))
        elif profile_class == 'poster' :
                context['jobs_status'] = "Successful Tasks"
                context['jobs']     = Job.objects.filter(creator=profile, is_done=True)
        return render_to_response('person/person_poster_jobs.html', context, context_instance=RequestContext(request))


def updateProfile(request):
        p=Person.objects.get(person=request.user)
        is_staff = request.user.is_staff
        if request.user.is_authenticated():
                if request.method == "POST":
                        form = UpdateInform(request.POST, request.FILES, instance=p)
                        if form.is_valid():
                                
                                form.save()
                                return HttpResponseRedirect('/')
                else:
                        form = UpdateInform(instance=p)
                context = {
                        'form':form,
                        'profile': p,
                        'is_staff': is_staff,
                        }
                return render_to_response('person/person_form.html', context, context_instance=RequestContext(request))
        else:
                return HttpResponseRedirect('/')