from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Department(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=400, blank=False, null=False)
	head = models.CharField(max_length=100,blank=False, null=False)
	contact = models.CharField(blank=False, null=False,max_length=10)
	def __unicode__(self):
		return '%s' % (self.title)

class Category(models.Model):
	category = models.CharField(max_length=300)
	def __unicode__(self):
		return '%s' % (self.category)

class Description(models.Model):
	category = models.ForeignKey(Category)
	description = models.TextField()
	def __unicode__(self):
		return '%s' % (self.description)

class WasteGenerated(models.Model):
	department = models.ForeignKey(Department)
	category = models.ForeignKey(Category)
	description = models.ForeignKey(Description)
	quantity = models.FloatField()
	date = models.DateField(auto_now_add = True)
	def __unicode__(self):
		return '%s' % (self.id)

class WasteStored(models.Model):
	department = models.ForeignKey(Department)
	category = models.ForeignKey(Category)
	description = models.ForeignKey(Description)
	quantity = models.FloatField()
	date = models.DateField(auto_now_add = True)
	def __unicode__(self):
		return '%s' % (self.id)

class WasteSentToRecycler(models.Model):
	department = models.ForeignKey(Department)
	category = models.ForeignKey(Category)
	description = models.ForeignKey(Description)
	quantity = models.FloatField()
	date = models.DateField(auto_now_add = True)
	def __unicode__(self):
		return '%s' % (self.id)

class UserSelections(models.Model):
	user = models.ForeignKey(User)
	category = models.ForeignKey(Category)
	description = models.ForeignKey(Description)
	def __unicode__(self):
		return '%s' % (self.id)

class UserActivated(models.Model):
	user = models.ForeignKey(User)
	activated = models.BooleanField(default = False)
