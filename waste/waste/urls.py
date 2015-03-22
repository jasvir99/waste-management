from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'waste.src.views.new_login', name='home'),
    url(r'^form', 'waste.src.views.main_form', name='home'),
    url(r'^add_selection', 'waste.src.views.add_selection'),
    url(r'^report', 'waste.src.views.generate_report'),
    url(r'^get_description', 'waste.src.views.get_description'),
    url(r'^add_profile', 'waste.src.views.add_profile'),
    url(r'^edit_profile', 'waste.src.views.edit_profile'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
