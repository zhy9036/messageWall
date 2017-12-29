from rest_framework.serializers import ModelSerializer
from message_api.models import Message


class MessageDetailSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['id',
                  'content',
                  'create_date',
                  ]


class MessageListSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['user_id',
                  'username',
                  'content',
                  'create_date'
                  ]

