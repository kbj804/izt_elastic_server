# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        '''
        chat/routing.py에 정의된 URL 파라미터에서 room_name을 얻습니다.
        즉 소비자에게 WebSocket 연결을 열어줍니다.
        참고로 모든 소비자들은 현재 인증된 유저, URL의 인자를 포함하여 연결에 대한 정보를 갖는 scope를 갖습니다.
        '''
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        
        # 사용자가 작성한 room 이름으로부터 채널의 그룹 이름을 짓습니다.
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        '''
        그룹에 join합니다.
        소비자들은 비동기 channel layer 메서드를 호출할 때 동기적으로 받아야 하기 때문에, async_to_sync(...) 같은 wrapper가 필요합니다.
        ( 모든 channel layer 메서드는 비동기입니다. )
        '''
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # WebSocket 연결을 받아들입니다
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        # 그룹을 떠납니다.
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        '''
        그룹에게 이벤트를 보냅니다.
        이벤트에는 이벤트를 수신하는 소비자가 호출해야 하는 메서드 이름에 대응하는 특별한 type 키가 있습니다.
        '''
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))