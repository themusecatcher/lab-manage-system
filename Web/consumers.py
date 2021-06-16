# 将消费者代码重写为异步，以提高其性能。\
from channels.generic.websocket import AsyncWebsocketConsumer
import json

#继承父类AsyncWebsocketConsumer
#使用WebSocket协议的异步通信方式实现浏览器和服务器之间的数据传递。
#(WebsocketConsumer)是以同步方式运行的
class ChatConsumer(AsyncWebsocketConsumer):
    # async语法能将函数方法以异步方式运行， 从而提高代码的运行速度和性能
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # 加入房间
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 离开房间
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 从WebSocket接收信息
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 向聊天室发送信息
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # 从聊天室接收信息
    async def chat_message(self, event):
        message = event['message']

        # 发送信息到WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
