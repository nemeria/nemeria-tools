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
    
    url(r'^$','nemeriatools.views.home'),
    # Vue liste + detail pour joueurs, alliances, villes
    url(r'^joueur/$','nemeriatools.views.joueur_index'),
    url(r'^joueur/(?P<joueur_autoinc>\d+)/$','nemeriatools.views.joueur_detail'),
    url(r'^alliance/$', 'nemeriatools.views.alliance_index'),
    url(r'^alliance/(?P<alliance_autoinc>\d+)/$','nemeriatools.views.alliance_detail'),
    url(r'^ville/$', 'nemeriatools.views.ville_index'),
    url(r'^ville/(?P<ville_autoinc>\d+)/$','nemeriatools.views.ville_detail'),
)
