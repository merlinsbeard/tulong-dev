from person.models import *
from django.contrib import admin
from job.models import Job


class JobInline(admin.TabularInline):
	model = Job	
	extra = 0

class Skills(admin.TabularInline):
	model = Person.skills.through
	extra = 1

class ProfileAdmin(admin.ModelAdmin):
	search_fields = ['person',]
	inlines = [JobInline,Skills]
	raw_fields = ("skills",)
	date_hierarchy = 'created_at'
	list_display = ['person',
			'person_class',
			'firstname','lastname',
			'is_verified',
			'created_at',]
	list_filter 	= ["person_class", 
							"is_verified", "created_at",
							]
	list_editable 	= ["is_verified",
							]
	prepopulated_fields = {
	"slug": ("person",)
	}

admin.site.register(PersonBadge)
admin.site.register(PersonClassification)
admin.site.register(Person, ProfileAdmin)
admin.site.register(PersonSkills)