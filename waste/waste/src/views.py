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

from waste.src.helper import calculate_generated
from waste.src.helper import calculate_stored
from waste.src.helper import calculate_sent
#from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
import itertools

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
		try:
			form_redirected = request.session.get('redirected')
			user = request.user
			form = UserSelectionForm(request=request)
			request.session['redirected'] = ''
			return render(request,'src/selection.html',{'form':form, 
				'form_redirected':form_redirected})
		except:
			user = request.user
			form = UserSelectionForm(request=request)
			return render(request,'src/selection.html',{'form':form})

@login_required
def add_profile(request):
	if request.method == 'POST':
		form = DepartmentProfileForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			head = form.cleaned_data['head']
			contact = form.cleaned_data['contact']
			user = request.user
			Department(user=user, title=title, head=head, contact=contact).\
			save()
			message = 'Profile Saved '
			return render(request,'src/success.html',{'message':message})
		else:
			form = DepartmentProfileForm(request.POST)
			return render(request, 'src/add_profile.html',{'form':form})

	else:
		user = request.user
		dept = Department.objects.filter(user=user.id)
		if dept:
			dept = Department.objects.get(user=user.id)
			return render(request, 'src/add_profile.html',{'dept':dept})
		else:
			try:
				form_redirected = request.session.get('redirected')
				user = request.user
				form = UserSelectionForm(request=request)
				request.session['redirected'] = ''
				form = DepartmentProfileForm()
				return render(request, 'src/add_profile.html',{'form':form,
					'form_redirected':form_redirected})
			except:
				form = DepartmentProfileForm()
				return render(request, 'src/add_profile.html',{'form':form})

@login_required
def main_form(request):
	if request.method == 'POST':
		user = request.user
		
		try:
			dept_form = DepartmentSelect(request.POST)
			if dept_form.is_valid():
				department = Department.objects.get(name = dept_form.cleaned_data['select_department'])
			else:
				department = Department.objects.get(user=user.id)
		except:
			department = Department.objects.get(user=user.id)
		for quantity, category, description in itertools.izip(request.POST.getlist("quantity"), request.POST.getlist("category"), request.POST.getlist("description")):
		#for quantity in request.POST.getlist("quantity") and category in request.POST.getlist("category"):
			cat = Category.objects.get(id=category)
			desc = Description.objects.get(id=description)
			WasteGenerated(department = department, quantity=quantity,category=cat, description=desc).save()

		message = 'Data Saved '
		return render(request,'src/success.html',{'message':message})

	else:
		user = request.user
		user_selections = UserSelections.objects.filter(user=user)
		if user_selections:
			pass
		else:
			request.session['redirected'] = 1
			return HttpResponseRedirect(reverse('waste.src.views.add_selection'))

		department = Department.objects.filter(user=user.id)
		if department:
			pass

		else:
			request.session['redirected'] = 1
			return HttpResponseRedirect(reverse('waste.src.views.add_profile'))
		dept_form = DepartmentSelect()
		waste_gen = WasteGeneratedForm(instance=WasteGenerated())
		#formsets = WasteFormSet()
		waste_stored = WasteStoredForm()
		waste_sent = WasteSentToRecyclerForm()
		category = Category.objects.all()
		description = Description.objects.all()
		forms = {'dept_form':dept_form,#'formset': formset,
		'waste_stored': waste_stored,'waste_sent':waste_sent,'user':user,
		'category': category,'description':description,'waste_gen':waste_gen}
		return render(request,'src/form.html',forms)


@login_required
def get_description(request):
	category = request.GET['cat_id']
	user = request.user
	description_dict = {}
	description_dict['0'] = '--------------'
	user_description = UserSelections.objects.values_list('description',flat=True).filter(category=category).\
		filter(user=user)
	description = Description.objects.filter(id__in = user_description)
	for value in description:
		description_dict[value.id] = value.description
	return HttpResponse(simplejson.dumps(description_dict))

@login_required
def generate_report(request):
	org = _ORGANISATION
	add = _ADDRESS
	is_superuser = request.user.is_superuser
	waste_generated = calculate_generated(request)
	waste_stored = calculate_stored(is_superuser,request)
	waste_sent = calculate_sent(request)
	return render(request,'src/report.html',{'waste_generated':waste_generated,
		'waste_sent':waste_sent,'waste_stored':waste_stored,'org':org,'add':add})



@login_required
def edit_profile(request):
	if request.method == 'POST':
		form = DepartmentProfileForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			head = form.cleaned_data['head']
			contact = form.cleaned_data['contact']
			user = request.user
			Department.objects.filter(user=user.id).update(user=user, title=title, head=head, contact=contact)
			message = 'Profile Saved '
			return render(request,'src/success.html',{'message':message})
		else:
			form = DepartmentProfileForm(request.POST)
			return render(request, 'src/add_profile.html',{'form':form})

	else:
		user = request.user
		dept = Department.objects.get(user=user.id)
		form = DepartmentProfileForm(instance=dept)
		return render(request, 'src/add_profile.html',{'form':form})

@login_required
def new_login(request):
	user = request.user
	active = UserActivated.objects.filter(user=user)
	if active:
		return HttpResponseRedirect(reverse('waste.src.views.main_form'))
	else:
		activate = UserActivated(user=user,activated=True)
		activate.save()
		return HttpResponseRedirect(reverse('waste.src.views.add_profile'))
