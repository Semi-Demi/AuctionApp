from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import AuctionItem

class AuctionConsumer(AsyncWebsocketConsumer):

    # Called when websocket connection is initiated
    # We set a group name to notify every connection within the bids group.
    async def connect(self):
        self.group_name = 'bids'

        await self.channel_layer.group_add(self.group_name, self.channel_name)


        await self.accept()

        print('connected')

    # When a websocket connection is closed
    # When it is closed we discard the group
    async def disconnect(self, code):
        print('disconnected')
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # This is called when we want to notify every registered user about a new highest bidder on an auction item
    # Here we prepare the data we want to display
    async def send_notif(self, event):
        print("in sender")
        bid_price = event['message']['bid_price']
        bidder_name = event['message']['bidder_name']
        auction_name = event['message']['auction_name']
        auction_ID = event['message']['auction_ID']

        message_sent = bidder_name + " has just bid $" + bid_price + " on auction " + auction_name + " with ID: " + auction_ID

        print("Sending to websocket")

            # Send the data to WebSocket so we can show the notification to users
        await self.send(text_data=json.dumps({
            'message_sent': message_sent
        }))

    async def send_winner(self, event):
        print("in sender")
        auction_name = event['message']['auction_name']
        auction_ID = event['message']['auction_ID']
        bidder_name = event['message']['bidder_name']
        bid_price = event['message']['bid_price']

        message_sent = bidder_name + " has won " + auction_name + " with ID: " + auction_ID + " with a bid of $" + bid_price
        print("Sending to websocket")

        # Send the data to WebSocket so we can show the notification to users
        await self.send(text_data=json.dumps({
            'message_sent': message_sent
        }))
