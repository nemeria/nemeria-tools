from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nemeria.views.home', name='home'),
    # url(r'^nemeria/', include('nemeria.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^pseudo/(?P<joueur_id>\d+)/$','nemeriatools.views.pseudo_detail'),
    url(r'^pseudo/$','nemeriatools.views.pseudo_index'),
)
