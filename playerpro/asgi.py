# # asgi.py

# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack

# from firstapp.consumers import ChatConsumer, EchoConsumer
# # from playerpro.routing import websocket_urlpatterns
# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'playerpro.settings.dev')

# # application = ProtocolTypeRouter({
# #     "http": get_asgi_application(),
# #     "websocket": AuthMiddlewareStack(
# #         URLRouter(
# #             os.path('ws/chat/', ChatConsumer)
# #         )
# #     ),
# # })


# # asgi.py

# import os
# from django.core.asgi import get_asgi_application
# from django.urls import path
# from firstapp import consumers

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

# application = get_asgi_application()

# # Define your ASGI routing
# application = ProtocolTypeRouter({
#     "websocket": URLRouter(
#         [
#             path("ws/chat/<str:room_name>/", consumers.ChatConsumer.as_asgi()),
#         ]
#     ),
# })



# # import os
# # from django.core.asgi import get_asgi_application


# # application = get_asgi_application()







from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import firstapp.routing

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'playerpro.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            firstapp.routing.websocket_urlpatterns
        )
    )
})
