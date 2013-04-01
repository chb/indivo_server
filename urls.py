from django.conf.urls import patterns, include

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Coding Systems
    (r'^codes/', include('codingsystems.urls')),
                       
    # Everything to indivo
    (r'^', include('indivo.urls.urls')),
)
