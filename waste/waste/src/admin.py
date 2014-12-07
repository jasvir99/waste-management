from django.contrib import admin
from waste.src.models import *
# Register your models here.
admin.autodiscover() 

admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Description)

