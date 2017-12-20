from django.contrib.auth.models import User, Group

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    password = serializers.CharField(source='user.password', write_only=True)

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'password')
        write_only_fields = ('password',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')