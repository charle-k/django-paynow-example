from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'paynow.views.index', name='index'),
    url(r'^paynow/', include('paynow.urls', namespace="paynow")),
    url('^login/', auth_views.login, {'template_name': 'paynow/login.html'}),
    url('^logout/', auth_views.logout, {'next_page': '/login/'}),
    url(r'^admin/', include(admin.site.urls)),
]
