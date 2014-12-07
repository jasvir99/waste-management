from django.db import models

# Create your models here.

class Department(models.Model):
	name = models.CharField(max_length=400)
	def __unicode__(self):
		return '%s' % (self.name)

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
