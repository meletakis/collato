# -*- coding: utf-8 -*-
import uuid

from django.forms import ModelForm
from applications.models import App, Data, Domain
from django.forms.models import inlineformset_factory
from django import forms
from django.forms.extras.widgets import *
from django.utils.translation import gettext as _
from responsibilities.models import Responsibility


class AppForm (ModelForm):
	name = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'size':'100' }))
	
	class Meta:
		model = App
		fields = ['name','description','domain','source_code_host','responsibility']
		
		
class DataApplicationForm (ModelForm):
	class Meta:
		model = Data
		fields = ['data_type','name', 'domain','description']
		exclude = ('app',)
		
#AppFormset = inlineformset_factory(Gadget, Data, fields=('data_name','input_type'), can_delete=False)		
		
class DomainForm (ModelForm):

	Name = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'size':'100' , 'placeholder':"Name"}))
	Description = forms.CharField( widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Description"}))

	class Meta:
		model = Domain



class AppForm2 (ModelForm):
	name = forms.CharField( label=_("Name"), widget=forms.TextInput(attrs={'class':'form-control',  }))
	description = forms.CharField(label=_("Description"), widget=forms.Textarea(attrs={'class':'form-control', 'rows':"2" }))
	domain = forms.ModelChoiceField( label=_("Domain"), queryset=Domain.objects.all(), widget=forms.Select(attrs={'class':'form-control',  }))
	source_code_host = forms.CharField(label= _("Source Code Host"), widget=forms.TextInput(attrs={'class':'form-control',  }))
	responsibility = forms.ModelChoiceField( label=_("Responsibility"), queryset=Responsibility.objects.all(), widget=forms.Select(attrs={'class':'form-control',  }))


	class Meta:
		model = App
		fields = ['name','description','domain','source_code_host','responsibility']
		
		
class DataApplicationForm2 (ModelForm):

	DATA_TYPE_CHOICES = (
    ("User_Input", _("User_Input")),
    ("Profile_Input", _("Profile_Input")),
    ("Application_Input", _("Application_Input")),
    ("Output", _("Output")), )


	data_type = forms.ChoiceField( label=_("Data Type"), choices = DATA_TYPE_CHOICES , widget=forms.Select( attrs={'class':'form-control',  }))	
	name = forms.CharField( label=_("Name"), widget=forms.TextInput(attrs={'class':'form-control',  }))
	description = forms.CharField( label=_("Description"), widget=forms.Textarea(attrs={'class':'form-control', 'rows':"2" }))
	domain = forms.ModelChoiceField( label=_("Domain"), queryset=Domain.objects.all(), widget=forms.Select(attrs={'class':'form-control',  }))	
	slug = forms.SlugField(label=_("Slug"), widget=forms.TextInput(attrs={'class':'form-control',  }))
	class Meta:
		model = Data
		fields = ['data_type','name', 'domain','description','slug']
		exclude = ('app',)

