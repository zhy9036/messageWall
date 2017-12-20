from rest_framework.serializers import ModelSerializer
from message_pool.models import Message


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['content',
                  'create_date',

                  ]


