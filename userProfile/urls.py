from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view),
    path('', views.logout_view, name='logout'),
]
