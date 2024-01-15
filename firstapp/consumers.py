# # # yourapp/consumers.py

# # import json
# # from asgiref.sync import async_to_sync
# # from channels.generic.websocket import WebsocketConsumer
# # from django.contrib.auth import get_user_model

# # User = get_user_model()

# # class ChatConsumer(WebsocketConsumer):
# #     def connect(self):
# #         self.room_name = self.scope['url_route']['kwargs']['room_name']
# #         self.room_group_name = f"chat_{self.room_name}"

# #         async_to_sync(self.channel_layer.group_add)(
# #             self.room_group_name,
# #             self.channel_name
# #         )

# #         self.accept()

# #     def disconnect(self, close_code):
# #         async_to_sync(self.channel_layer.group_discard)(
# #             self.room_group_name,
# #             self.channel_name
# #         )

# #     def receive(self, text_data):
# #         text_data_json = json.loads(text_data)
# #         message = text_data_json['message']
# #         username = self.scope["user"].username

# #         async_to_sync(self.channel_layer.group_send)(
# #             self.room_group_name,
# #             {
# #                 'type': 'chat.message',
# #                 'message': message,
# #                 'username': username,
# #             }
# #         )

# #     def chat_message(self, event):
# #         message = event['message']
# #         username = event['username']

# #         self.send(text_data=json.dumps({
# #             'message': message,
# #             'username': username,
# #         }))


# from channels.consumer import SyncConsumer

# class EchoConsumer(SyncConsumer):
#     def websocket_connect(self, event):
#         print("Connect event is called")
#         print(event)

#     def websocket_receive(self, event):
#         print("New event is received")
#         print(event)

# # consumers.py

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']

#         await self.send(text_data=json.dumps({
#             'message': message
#         }))







from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        # self.send(text_data=json.dumps({
        #     'type':'connection is good',
        #     'message':'you are connected now bitch!'
        # }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']
        print('content from receive')
        print(content)
        print(sender)
        print(sender)
        print(sender)
        # self.send(text_data=json.dumps({
        #     'type':'chat',
        #     'content':content,
        #     'sender':sender
        # }))

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'content':content,
                'sender':sender, 
                'receiver':receiver
            }
        )
    def chat_message(self, event):
        message = event['content']
        sender = event['sender']
        receiver = event['receiver']
        print('dit is van chat_message')
        print(message)
        self.send(text_data=json.dumps({
            'type':'chat',
            'content':message,
            'sender':sender,
            'receiver':receiver

        }))

    # def chat_message(self, event):
    #     message = event['message']
    #     username = event['username']

    #     self.send(text_data=json.dumps({
    #         'message': message,
    #         'username': username,
    #     }))
