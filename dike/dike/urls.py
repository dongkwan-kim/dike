"""dike URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from webdike import views as view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^base/', view.base),
    url(r'^$', view.home),
    url(r'^judgement/([\d]+)/', view.get_judgement),
    url(r'^editor/split/([\d]+)/', view.get_splitter),
    url(r'^editor/polish/([\d]+)/', view.get_polisher),
    url(r'^editor/connect/([\d]+)/', view.get_connector),
    url(r'^editor/explain/([\d]+)/', view.get_explainer),
    url(r'^vote$', view.get_voter),
    url(r'^step/([\d]+)/', view.save_step),
    url(r'^accounts/', include('allauth.urls'))
]
