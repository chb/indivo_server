from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Coding Systems
    (r'^codes/', include('indivo_server.codingsystems.urls')),
                       
    # Everything to indivo
    (r'^', include('indivo_server.indivo.urls.urls')),
)
