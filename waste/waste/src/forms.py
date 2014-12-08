from django import forms
from waste.src.models import *
from django.db.models import Q

class DepartmentSelect(forms.Form):
	select_department = forms.ModelChoiceField(queryset=Department.objects.all())
	def __init__(self, *args, **kwargs):
		super(DepartmentSelect, self).__init__(*args, **kwargs)
		self.fields['select_department'].widget.attrs={'id': 'department','class':'btn btn-default dropdown-toggle'}

class WasteGeneratedForm(forms.Form):
	try:
		generated_waste_category = forms.ModelChoiceField(queryset=Category.objects.all())
		generated_waste_description = forms.ModelChoiceField(queryset = Description.objects.all())
		generated_waste_quantity = forms.FloatField()
	except:
		pass

	def __init__(self, *args, **kwargs):
		super(WasteGeneratedForm, self).__init__(*args, **kwargs)
		self.fields['generated_waste_category'].widget.attrs={'id': 'gen_category', 'class':'btn btn-default dropdown-toggle'}
		self.fields['generated_waste_description'].widget.attrs={'id':'gen_description','class':'btn btn-default dropdown-toggle'}
		self.fields['generated_waste_quantity'].widget.attrs={'id':'gen_quantity','placeholder':'Kilogram'}

class WasteStoredForm(forms.Form):
	try:
		stored_waste_category = forms.ModelChoiceField(queryset=Category.objects.all())
		stored_waste_description = forms.ModelChoiceField(queryset = Description.objects.all())
		stored_waste_quantity = forms.FloatField()
	except:
		pass

	def __init__(self, *args, **kwargs):
		super(WasteStoredForm, self).__init__(*args, **kwargs)
		self.fields['stored_waste_category'].widget.attrs={'id': 'store_category','class':'btn btn-default dropdown-toggle'}
		self.fields['stored_waste_description'].widget.attrs={'id':'store_description','class':'btn btn-default dropdown-toggle'}
		self.fields['stored_waste_quantity'].widget.attrs={'id':'store_quantity','placeholder':'Kilogram'}

class WasteSentToRecyclerForm(forms.Form):
	try:
		sent_waste_category = forms.ModelChoiceField(queryset=Category.objects.all())
		sent_waste_description = forms.ModelChoiceField(queryset = Description.objects.all())
		sent_waste_quantity = forms.FloatField()
	except:
		pass

	def __init__(self, *args, **kwargs):
		super(WasteSentToRecyclerForm, self).__init__(*args, **kwargs)
		self.fields['sent_waste_category'].widget.attrs={'id': 'sent_category','class':'btn btn-default dropdown-toggle'}
		self.fields['sent_waste_description'].widget.attrs={'id':'sent_description','class':'btn btn-default dropdown-toggle'}
		self.fields['sent_waste_quantity'].widget.attrs={'id':'sent_quantity','placeholder':'Kilogram'}

class UserSelectionForm(forms.Form):
	try:
		user = request.user
	except:
		user = 1
	desc_id = UserSelections.objects.values_list('description', flat=True).filter(user=user)
	information_technology_and_telecommunication_equipment = forms.\
	ModelMultipleChoiceField(required=True,widget=forms.CheckboxSelectMultiple,\
	queryset= Description.objects.filter(category = 1).filter(~Q(id__in=desc_id)))

	consumer_electrical_and_electronics = forms.ModelMultipleChoiceField(required = \
		True, widget = forms.CheckboxSelectMultiple, queryset = Description.\
		objects.filter(category = 2).filter(~Q(id__in=desc_id)))