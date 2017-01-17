from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from person.models import Person, PersonSkills
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from datetime import date
from django.forms.extras.widgets import SelectDateWidget


year = date.today().year
years = range(1920, year-10)
years = [str(i) for i in years]
BIRTH_YEAR_CHOICES = years

class RegistrationForm(ModelForm):
        email           = forms.EmailField(label=(u'Email Address / Username'), 
                                widget=forms.TextInput(attrs={"placeholder":"hello@gmail.com"}))
        password        = forms.CharField(label=(u'Password'), 
                                widget=forms.PasswordInput(render_value=False))
        password1       = forms.CharField(label=(u'Verify Password'), 
                                widget=forms.PasswordInput(render_value=False))
        firstname       = forms.CharField(label=(u'Firstname'))
        lastname        = forms.CharField(label=(u'Lastname'))
        contactno       = forms.CharField(label=(u'Contact No:'))
        birthday        = forms.DateField(label=(u'Birthday'),
                                widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES,
                                        attrs={'class': 'form-control input',}))
        address         = forms.CharField(label=(u'Address'),
                                    widget=forms.Textarea(attrs={"placeholder":"Address", 
                                                            "rows": 3,}))
        skills = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, 
                                        queryset=PersonSkills.objects.all(), required=False)
        terms = forms.BooleanField(
                    error_messages={'required': 'You must accept the terms and conditions'},
                    label="Terms & Conditions"
                )

        def __init__(self, *args, **kwargs):
            super(RegistrationForm, self).__init__(*args, **kwargs)
            self.fields['email'].widget.attrs['class'] = 'form-control input-large'
            self.fields['firstname'].widget.attrs['class'] = 'form-control input-large'
            self.fields['lastname'].widget.attrs['class'] = 'form-control input-large'
            self.fields['contactno'].widget.attrs['class'] = 'form-control input-large'
            self.fields['address'].widget.attrs['class'] = 'form-control'
            self.fields['password'].widget.attrs['class'] = 'form-control input-large'
            self.fields['password1'].widget.attrs['class'] = 'form-control input-large'

        class Meta:
                model = Person
                exclude = (
                        'image',
                        'contactno',
                        'image',
                        'birthday',
                        'person',
                        'is_verified',
                        'is_active',
                        'firstname',
                        'lastname',
                        'slug',
                        'created_at',
                        'address',
                        'info',
                        'person_class',
                        'classification',
                        )

        def clean_contactno(self):
            clean_contactno = self.cleaned_data['contactno']
            if len(clean_contactno) != 10:
                raise forms.ValidationError("Number must be exactly 10 digits long")
            elif clean_contactno[0] != '9':
                raise forms.ValidationError("Mobile Number is Invalid, must start with 9 ")
            else:
                return clean_contactno


        def clean_email(self):
                email = self.cleaned_data['email']
                try:
                        User.objects.get(username=email)
                except User.DoesNotExist:
                        return email
                raise forms.ValidationError("That email is already taken, please select another.")
   
        def clean_birthday(self):
                birthday = self.cleaned_data['birthday']
                days_in_year = 365.25
                today = date.today()
                age = int((today-birthday).days/days_in_year)
                if age < 18:
                        raise forms.ValidationError("You need to be 18 and above to use this service")
                else:
                        return birthday

        def clean(self):
                try:
                        password = self.cleaned_data['password']
                        password1 = self.cleaned_data['password1']
                        if self.cleaned_data['password'] != self.cleaned_data['password1']:
                                raise forms.ValidationError("The passwords did not match.  Please try again.")
                        elif len(self.cleaned_data['password']) < 6:
                                raise forms.ValidationError("Password must be 8 characters long")
                except KeyError:
                        raise forms.ValidationError('The password field was blank')
                return self.cleaned_data

class LoginForm(forms.Form):
        username        = forms.CharField(label=(u'Emails'))
        password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))

       