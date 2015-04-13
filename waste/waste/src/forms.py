from django import forms
from waste.src.models import *
from django.db.models import Q

class DepartmentSelect(forms.Form):
	select_department = forms.ModelChoiceField(queryset=Department.objects.all())
	def __init__(self, *args, **kwargs):
		super(DepartmentSelect, self).__init__(*args, **kwargs)
		self.fields['select_department'].widget.attrs={'id': 'department','class':'btn btn-default dropdown-toggle'}

class WasteGeneratedForm(forms.ModelForm):
	#try:
		#generated_waste_category = forms.ModelChoiceField(queryset=Category.objects.all())
		#generated_waste_description = forms.ModelChoiceField(queryset = Description.objects.all())
	quantity = forms.FloatField()
	#except:
		#pass

	class Meta:
		model = WasteGenerated
		#exclude = ['department',]
		
		fields = ["quantity", "category", "description","department"]
		widgets = {
      'category': forms.HiddenInput(),
	  'description': forms.HiddenInput(),
	  'department': forms.HiddenInput(),
	
    }

		'''def __init__(self, *args, **kwargs):
			is_hidden = kwargs.pop('is_hidden', None)
			super(WasteGeneratedForm, self).__init__(*args, **kwargs)
			self.fields['quantity'].widget.attrs={'id':'quantity','placeholder':'Kilogram'}
			if is_hidden:
				self.fields['category'].widget = forms.HiddenInput()
				self.fields['description'].widget = forms.HiddenInput()
				self.fields['department'].widget = forms.HiddenInput()'''

	'''def __init__(self, *args, **kwargs):
		super(WasteGeneratedForm, self).__init__(*args, **kwargs)
		#self.fields['generated_waste_category'].widget.attrs={'id': 'gen_category', 'class':'btn btn-default dropdown-toggle'}
		#self.fields['generated_waste_description'].widget.attrs={'id':'gen_description','class':'btn btn-default dropdown-toggle'}
		self.fields['generated_waste_quantity'].widget.attrs={'id':'gen_quantity','placeholder':'Kilogram'}'''

	'''def __init__(self, *args, **kwargs):
		super(WasteGeneratedForm, self).__init__(*args, **kwargs)
        #combine object_type and object_id into a single 'generic_obj' field
        #getall the objects that we want the user to be able to choose from
		waste_category = list(Category.objects.all()) #put your stuff here
       
        #now create our list of choices for the <select> field
		waste = []
		for wc in waste_category:
			waste_description = Description.objects.get(id=1)
		#	for wd in waste_description:
			wc_id = wc.id
			form_value = "type:%s-id:%s" % (wc_id, waste_description.id) #e.g."type:12-id:3"
			display_text = str(wc)
			waste.append([form_value, display_text])
		
		self.fields['generated_waste_quantity'].widget.attrs=waste
	
	class Meta:
		model = WasteGenerated
		fields = [
			"generated_waste_quantity"
		]

	def save(self, *args, **kwargs):
        #get object_type and object_id values from combined generic_obj field
		object_string = self.cleaned_data['generated_waste_quantity']
		matches = re.match("type:(\d+)-id:(\d+)", object_string).groups()
		category_id = matches[0] #get 45 from "type:45-id:38"
		description_id = matches[1] #get 38 from "type:45-id:38"
		generated_waste_category = Category.objects.get(id=category_id)
		generated_waste_description = Description.objects.get(id=description_id)
		self.cleaned_data['generated_waste_category'] = category_id
		self.cleaned_data['generated_waste_description'] = description_id
		self.instance.generated_waste_category = category_id
		self.instance.generated_waste_description = description_id
		return super(WasteGeneratedForm, self).save(*args, **kwargs)'''

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
	information_technology_and_telecommunication_equipment = forms.\
		ModelMultipleChoiceField(required=True,widget=forms.CheckboxSelectMultiple,queryset = None)

	consumer_electrical_and_electronics = forms.ModelMultipleChoiceField(required = \
			True, widget = forms.CheckboxSelectMultiple,queryset = None)

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		user = self.request.user
		desc_id = UserSelections.objects.values_list('description', flat=True).filter(user=user)
		super(UserSelectionForm, self).__init__(*args, **kwargs)
		self.fields['information_technology_and_telecommunication_equipment'].\
			queryset= Description.objects.filter(category = 1).filter(~Q(id__in=desc_id))
		self.fields['consumer_electrical_and_electronics'].\
			queryset= Description.objects.filter(category = 2).filter(~Q(id__in=desc_id))

class DepartmentProfileForm(forms.ModelForm):
	class Meta:
		model = Department
		exclude = ['user']
