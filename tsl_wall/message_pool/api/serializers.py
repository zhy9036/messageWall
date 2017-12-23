from rest_framework.serializers import ModelSerializer
from message_pool.models import Message


class MessageDetailSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['id',
                  'user',
                  'content',
                  'create_date',
                  ]


class MessageListSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['user',
                  'content',
                  'create_date'
                  ]

