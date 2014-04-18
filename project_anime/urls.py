from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/', include('api.urls')),
)

urlpatterns += patterns('',
    url(r'^api-auth-token/', 'rest_framework.authtoken.views.obtain_auth_token'),
)
