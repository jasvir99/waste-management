from waste.src.models import *
from django.db.models import Sum

def calculate_generated():
	categories = WasteGenerated.objects.values_list('category_id',flat=True).distinct()
	generated = []
	for val in categories:
		temp = {}
		desc = WasteGenerated.objects.values_list('description__description',flat=True).\
			filter(category = val).distinct()
		category = Category.objects.values('category').filter(id = val)[0]
		total = WasteGenerated.objects.filter(category=val).aggregate(Sum('quantity'))
		temp['desc'] = desc
		temp['category'] = category
		temp['total'] = total['quantity__sum']
		generated.append(temp)
	return generated

def calculate_stored():
	categories = WasteStored.objects.values_list('category_id',flat=True).distinct()
	generated = []
	for val in categories:
		temp = {}
		desc = WasteStored.objects.values_list('description__description',flat=True).\
			filter(category = val).distinct()
		category = Category.objects.values('category').filter(id = val)[0]
		total = WasteStored.objects.filter(category=val).aggregate(Sum('quantity'))
		temp['desc'] = desc
		temp['category'] = category
		temp['total'] = total['quantity__sum']
		generated.append(temp)
	return generated

def calculate_sent():
	categories = WasteSentToRecycler.objects.values_list('category_id',flat=True).distinct()
	generated = []
	for val in categories:
		temp = {}
		desc = WasteSentToRecycler.objects.values_list('description__description',flat=True).\
			filter(category = val).distinct()
		category = Category.objects.values('category').filter(id = val)[0]
		total = WasteSentToRecycler.objects.filter(category=val).aggregate(Sum('quantity'))
		temp['desc'] = desc
		temp['category'] = category
		temp['total'] = total['quantity__sum']
		generated.append(temp)
	return generated