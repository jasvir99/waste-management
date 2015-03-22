from waste.src.models import *
from django.db.models import Sum

def calculate_generated(request):
	user = request.user
	if user.is_superuser:
		categories = WasteGenerated.objects.values_list('category_id',flat=True).\
			distinct()
	else:
		dept = Department.objects.get(user=user.id)
		categories = WasteGenerated.objects.filter(department=dept.id).values_list('category_id',flat=True).\
			distinct()
	generated = []
	for val in categories:
		temp = {}
		desc = WasteGenerated.objects.values_list('description__description',flat=True).\
			filter(category = val).distinct()
		category = Category.objects.values('category').filter(id = val)[0]
		try:
			total = WasteGenerated.objects.filter(department=dept.id).filter(category=val).aggregate(Sum('quantity'))
		except:
			total = WasteGenerated.objects.filter(category=val).aggregate(Sum('quantity'))
		temp['desc'] = desc
		temp['category'] = category
		temp['total'] = total['quantity__sum']
		generated.append(temp)
	return generated

def calculate_stored(super_user,request):
	if super_user == True:
		categories = WasteStored.objects.values_list('category_id',flat=True).distinct()
	else:
		user = request.user
		dept = Department.objects.get(user=user.id)
		categories = WasteStored.objects.filter(department=dept.id).values_list('category_id',flat=True).\
			distinct()

	generated = []
	for val in categories:
		temp = {}
		desc = WasteStored.objects.values_list('description__description',flat=True).\
			filter(category = val).distinct()
		category = Category.objects.values('category').filter(id = val)[0]
		try:
			total = WasteStored.objects.filter(department=dept.id).filter(category=val).aggregate(Sum('quantity'))
		except:
			total = WasteStored.objects.filter(category=val).aggregate(Sum('quantity'))

		temp['desc'] = desc
		temp['category'] = category
		temp['total'] = total['quantity__sum']
		generated.append(temp)
	return generated

def calculate_sent(request):
	user = request.user
	if user.is_superuser:
		categories = WasteSentToRecycler.objects.values_list('category_id',flat=True).distinct()
	else:
		dept = Department.objects.get(user=user.id)
		categories = WasteSentToRecycler.objects.filter(department=dept.id).\
		values_list('category_id',flat=True).distinct()
	generated = []
	for val in categories:
		temp = {}
		desc = WasteSentToRecycler.objects.values_list('description__description',flat=True).\
			filter(category = val).distinct()
		category = Category.objects.values('category').filter(id = val)[0]
		try:
			total = WasteSentToRecycler.objects.filter(department=dept.id).filter(category=val).aggregate(Sum('quantity'))
		except:
			total = WasteSentToRecycler.objects.filter(category=val).aggregate(Sum('quantity'))
		temp['desc'] = desc
		temp['desc'] = desc
		temp['category'] = category
		temp['total'] = total['quantity__sum']
		generated.append(temp)
	return generated