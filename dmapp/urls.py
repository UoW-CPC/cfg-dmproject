# dmapp/urls.py
from django.conf.urls import url
from dmapp import views


urlpatterns = [
    url(r'^dashboard/$', views.DMDashboardPageView.as_view())
]
