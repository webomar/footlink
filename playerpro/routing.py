# # routing.py

# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import playerpro.routing
# from django.urls import path
# from firstapp.consumers import EchoConsumer
# # application = ProtocolTypeRouter({
# #     'websocket': AuthMiddlewareStack(
# #         URLRouter(
# #             firstapp.routing.websocket_urlpatterns
# #         )
# #     ),
# # })
# from firstapp import consumers
# application = URLRouter([
#     path('ws/chat/', EchoConsumer)
# ])

# application = ProtocolTypeRouter({
#     "websocket": URLRouter(
#         [
#             path("ws/chat/<str:room_name>/", consumers.ChatConsumer.as_asgi()),
#         ]
#     ),
# })
# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from firstapp import consumers

application = ProtocolTypeRouter({
    "websocket": URLRouter(
        [
            path("ws/chat/<str:room_name>/", consumers.ChatConsumer.as_asgi()),
        ]
    ),
})
