from django.urls import path
from . import views
import auctions.views

app_name = 'userProfile'
urlpatterns = [
    path('', views.profile_view),
    path('', views.logout_view, name='logout'),
    path('<uuid:itemId>', auctions.views.checkAuction, name='checkAuction'),
]
