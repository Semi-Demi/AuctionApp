from channels.generic.websocket import AsyncWebsocketConsumer
import json

from channels.layers import channel_layers


class AuctionConsumer(AsyncWebsocketConsumer):

    #Called when websocket connection is initiated
    async def connect(self):
        await self.channel_layer.group_add('bids', self.channel_name)
        print('connected')
        print()
        await self.accept()

    #When a websocket connection is closed
    async def disconnect(self, code):
        print('disconnected')
        await self.channel_layer.group_discard('bids', self.channel_name)

    async def receive(self, text_data):
        print('receive')
        text_data_json = json.loads(text_data)
        bidPrice = text_data_json['bidPrice']
        timeLeft = text_data_json['timeLeft']
        message = text_data_json['message']

        await self.channel_layer.group_send(
            "bids",
            {
                "type": "send.notif",
                "bidPrice": bidPrice,
                "timeLeft": timeLeft,
                "message": message
            }
        )

    async def send_notif(self, event):
        bidder = event['message']['bidder']
        bid_price = event['message']['bid_price']
        auction_name = event['message']['auction_name']
        auction_id = event['message']['auction_id']
        remaining_time = event['message']['remaining_time']

        # Send the data to WebSocket
        await self.send(text_data=json.dumps({
            'bidder': bidder,
            'bid_price': bid_price,
            'auction_name': auction_name,
            'auction_id': auction_id,
            'remaining_time': remaining_time
        }))
