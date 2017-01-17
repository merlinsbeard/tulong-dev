from django import forms

class ContactForm(forms.Form):
	"""docstring for ContactUsForm"""
	name = forms.CharField()
	email = forms.EmailField()
	#mobile_number = forms.CharField(required=False, max_length=10, min_length=10)
	message = forms.CharField(widget=forms.Textarea(
					attrs={'rows':5,'class': 'form-control',}))
	
	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		lists = [
			['name','Bj Paat'],
			['email','bjpaat01@gmail.com'],
			#['mobile_number','9179071139'],
			]
		for field, placeholder in lists:
			self.fields[field].widget.attrs['class'] = 'form-control input-large'
			self.fields[field].widget.attrs['placeholder'] = placeholder
	'''
	def clean_mobile_number(self):
		mobile_number = self.cleaned_data['mobile_number']
		if len(mobile_number) != 10:
			raise forms.ValidationError("Number must be exactly 10 digits long")
		elif mobile_number[0] != '9':
			raise forms.ValidationError("Mobile Number is Invalid, must start with 9 ")
		else:
			return mobile_number
	'''