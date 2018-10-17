# homeapp/urls.py
from django.conf.urls import url
from homeapp import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^register/$', views.RegisterPageView.as_view()),
]
