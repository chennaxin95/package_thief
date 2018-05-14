# howdy/urls.py

from django.conf.urls import url
from django.urls import include, path
from howdy import views

urlpatterns = [
	url(r'$', views.HomePageView.as_view()),
	url(r'^about/$', views.AboutPageView.as_view()),
	 # Add this /about/ route
	# path('/', views.HomePageView.as_view()),
	# path('/about', views.AboutPageView.as_view()),
]
