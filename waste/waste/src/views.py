from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from waste.src.forms import *
from waste.src.models import *
from django.contrib.auth.decorators import login_required
import simplejson

# Create your tests here.
@login_required
def main_form(request):
	if request.method == 'POST':
		dept_form = DepartmentSelect(request.POST)
		waste_gen = WasteGeneratedForm(request.POST)
		waste_stored = WasteStoredForm(request.POST)
		waste_sent = WasteSentToRecyclerForm(request.POST)
		if dept_form.is_valid():
			department = Department.objects.get(name = dept_form.cleaned_data['select_department'])
		if waste_gen.is_valid():
			category = Category.objects.get(category=waste_gen.cleaned_data['generated_waste_category'])
			description = Description.objects.get(description=waste_gen.cleaned_data['generated_waste_description'])
			quantity = waste_gen.cleaned_data['generated_waste_quantity']
			generated = WasteGenerated(department = department,category = category,\
				description = description, quantity = quantity)
			generated.save()

		if waste_stored.is_valid():
			category = Category.objects.get(category=waste_stored.cleaned_data['stored_waste_category'])
			description = Description.objects.get(description=waste_stored.cleaned_data['stored_waste_description'])
			quantity = waste_stored.cleaned_data['stored_waste_quantity']
			stored = WasteStored(department = department,category = category,\
				description = description, quantity = quantity)
			stored.save()

		if waste_sent.is_valid():
			category = Category.objects.get(category=waste_sent.cleaned_data['sent_waste_category'])
			description = Description.objects.get(description=waste_sent.cleaned_data['sent_waste_description'])
			quantity = waste_sent.cleaned_data['sent_waste_quantity']
			sent = WasteSentToRecycler(department = department,category = category,\
				description = description, quantity = quantity)
			sent.save()
			
			return render(request,'src/success.html',{})

	else:
		dept_form = DepartmentSelect()
		waste_gen = WasteGeneratedForm()
		waste_stored = WasteStoredForm()
		waste_sent = WasteSentToRecyclerForm()
		forms = {'dept_form':dept_form,'waste_gen': waste_gen,
		'waste_stored': waste_stored,'waste_sent':waste_sent}
		return render(request,'src/form.html',forms)

def get_description(request):
	category = request.GET['cat_id']
	description_dict = {}
	description_dict['0'] = '--------------'
	description = Description.objects.filter(category=category)
	for value in description:
		description_dict[value.id] = value.description
	return HttpResponse(simplejson.dumps(description_dict))
