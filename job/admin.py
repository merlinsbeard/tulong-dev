from job.models import *
from django.contrib import admin
from bid.models import Bid
from comment.models import Comment
from discussion.models import Discussion
from easy_maps.widgets import AddressWithMapWidget
from django import forms

admin.site.register(JobType)
admin.site.register(JobDuration)

class BidInline(admin.TabularInline):
	model = Bid	
	extra = 1

class CommentInline(admin.TabularInline):
	model = Comment	
	extra = 1

class DiscussionInline(admin.TabularInline):
	model = Discussion
	extra = 1

class JobAdmin(admin.ModelAdmin):

	#Views the map Needs to have input in order to work	
	class form(forms.ModelForm):
		class Meta:
			widgets = {
			    #'gmap': AddressWithMapWidget({'class': 'vTextField'})
				'gmap': LocationWidget(),
			}
	
	search_fields = ['^content', '^city', '^title']
	inlines = [BidInline, CommentInline, DiscussionInline ]
	prepopulated_fields = {"slug": ("title","amount")}
	list_display 		= [
						"creator", "title",
						"amount", "is_published",
						"is_payed", "is_done", "is_close",
						"created_at", "updated_at"
							]
	list_filter 		= [ 
						"is_published", "is_payed",
						"is_close",
						"created_at", "date_need",
						"city",
							]

	list_editable 		= ["is_close", "is_payed", "is_done", ]


admin.site.register(JobWorker)
admin.site.register(Job, JobAdmin)