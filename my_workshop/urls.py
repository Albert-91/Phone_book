"""my_workshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from phone_book.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^new/', AddPerson.as_view(), name="add"),
    url(r'^adres/', ShowAll.as_view(), name="all"),
    url(r'^groups/', GroupsView.as_view(), name="groups"),
    url(r'^AddGroup/', AddGroup.as_view(), name="add_group"),
    url(r'^person/(?P<id>[0-9]+)/', ShowDetail.as_view(), name="person"),
    url(r'^modify/(?P<id>\d+)$', ModifyPerson.as_view(), name="modify"),
    url(r'^Delete/(?P<data>\w+)/(?P<id>\d+)$', DeleteData.as_view(), name="delete"),
    url(r'^Members/(?P<id>\d+)$', Members.as_view(), name="members"),
    url(r'^(?P<id>\d+)/AddAddress/$', AddAddress.as_view(), name="add_address"),
    url(r'^(?P<id>\d+)/AddPhone/$', AddPhone.as_view(), name="add_phone"),
    url(r'^(?P<id>\d+)/AddEmail/$', AddEmail.as_view(), name="add_email"),
    url(r'^(?P<id>\d+)/AddToGroup/$', AddToGroup.as_view(), name="add_to_group"),
]
