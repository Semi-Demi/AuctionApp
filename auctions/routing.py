from django.urls import path
from .consumers import AuctionConsumer

websocket_urlpatterns = [
    path('ws/auctions/', AuctionConsumer.as_asgi()),
]