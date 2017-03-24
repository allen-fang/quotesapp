from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), # renders index page
    url(r'^dashboard$', views.dashboard), # renders dashboard page
    url(r'^process_logreg$', views.process_logreg), # validates login and registration
    url(r'^logout$', views.logout), # logs user out
    url(r'^add$', views.addQuote), # routes from adding a quote
    url(r'^add_favorite/(?P<id>\d+)$', views.addFavorite), # adds favorite quote
    url(r'^remove_favorite/(?P<id>\d+)$', views.removeFavorite), # removes from favorite list
    url(r'^users/(?P<id>\d+)$', views.user), # directs to user page
]