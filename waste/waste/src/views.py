from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from waste.src.forms import *
from waste.src.models import *
from waste.config import _ORGANISATION
from waste.config import _ADDRESS
from django.contrib.auth.decorators import login_required
import simplejson
from django.db.models import Sum
from django.core.urlresolvers import reverse

# Create your tests here.
@login_required
def add_selection(request):
	if request.method == 'POST':
		user = request.user
		list_it = request.POST.\
			getlist('information_technology_and_telecommunication_equipment')
		for id in list_it:
			category = Category.objects.get(pk=1)
			description = Description.objects.get(pk=id)
			selections = UserSelections(user = user, category = category, \
				description = description)
			selections.save()
		list_elect = request.POST.getlist('consumer_electrical_and_electronics')
		for id in list_elect:
			category = Category.objects.get(pk=2)
			description = Description.objects.get(pk=id)
			selections = UserSelections(user = user, category = category, \
				description = description)
			selections.save()

		message = 'Selections Saved '
		return render(request,'src/success.html',{'message':message})
	else:
		user = request.user
		form = UserSelectionForm(request=request)
		return render(request,'src/selection.html',{'form':form})

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
			
			message = 'Data Saved '
			return render(request,'src/success.html',{'message':message})

	else:
		user = request.user
		user_selections = UserSelections.objects.filter(user=user)
		if user_selections:
			pass
		else:
			return HttpResponseRedirect(reverse('waste.src.views.add_selection'))
		dept_form = DepartmentSelect()
		waste_gen = WasteGeneratedForm()
		waste_stored = WasteStoredForm()
		waste_sent = WasteSentToRecyclerForm()
		forms = {'dept_form':dept_form,'waste_gen': waste_gen,
		'waste_stored': waste_stored,'waste_sent':waste_sent}
		return render(request,'src/form.html',forms)

def get_description(request):
	category = request.GET['cat_id']
	user = request.user
	description_dict = {}
	description_dict['0'] = '--------------'
	user_description = UserSelections.objects.values_UserActivatedlist('description',flat=True).filter(category=category).\
		filter(user=user)
	description = Description.objects.filter(id__in = user_description)
	for value in description:
		description_dict[value.id] = value.description
	return HttpResponse(simplejson.dumps(description_dict))

def generate_report(request):
	org = _ORGANISATION
	add = _ADDRESS
	waste_generated = WasteGenerated.objects.all().aggregate(Sum('quantity'))
	waste_stored = WasteStored.objects.all().aggregate(Sum('quantity'))
	waste_sent = WasteSentToRecycler.objects.all().aggregate(Sum('quantity'))
	return render(request,'src/report.html',{'waste_generated':waste_generated,
		'waste_sent':waste_sent,'waste_stored':waste_stored,'org':org,'add':add})

@login_required
def new_login(request):
	user = request.user
	active = UserActivated.objects.filter(user=user)
	if active:
		return HttpResponseRedirect(reverse('waste.src.views.main_form'))
	else:
		activate = UserActivated(user=user,activated=True)
		activate.save()
		return HttpResponseRedirect(reverse('admin:password_change'))
