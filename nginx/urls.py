"""MiliOPS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'get_proxy_server/$', views.GetProxyServer, name="get_proxy_server"),
    url(r'get_proxy_server_byproxyservergroup/$', views.GetProxyServerByGroup, name="get_proxy_server_byproxyservergroup"),
    url(r'updown_realserver/$', views.UpDownRealserver, name="updown_realserver"),
    url(r'search_site/$', views.SearchSite, name="search_site"),
    url(r'maintain/$', views.Maintain, name="maintain"),
    url(r'index/$', views.index, name="nginx_index"),
    # url(r'404/$', views.page_not_found),
    # url(r'500/$', views.page_error),
    url(r'^$', views.root),
]
