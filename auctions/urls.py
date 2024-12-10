from django.urls import path
from . import views

app_name = 'auctions'

urlpatterns = [
    path('', views.auctions_list, name='list'),
    path('<uuid:itemId>', views.auction_page, name='page'),

    path('new-auction/', views.auction_new, name='newAuction'),

    path('<uuid:itemId>/check', views.checkAuction, name='checkAuction'),
    path('<uuid:itemId>/time', views.calculateCountdown, name='countdown'),
    path('<uuid:itemId>/status', views.setStatus, name='status'),
]
