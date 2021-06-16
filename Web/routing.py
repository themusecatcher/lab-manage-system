from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from .urls import websocket_urlpatterns

#实例化中需要传入Channels的路由对象websocket_urlpatterns
#该对象把Django与Channels建立连接
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    #字典的key为websocket，代表使用WebSocket协议
    #字典的value是Channels的路由对象websocket_urlpatterns
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})