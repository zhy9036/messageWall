from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.status import HTTP_401_UNAUTHORIZED

from .serializers import UserSerializer, GroupSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes, detail_route
from rest_framework.response import Response
from django.contrib.sessions.models import Session
from django.utils import timezone


def get_all_logged_in_users_ids():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))
    return uid_list



#@permission_classes((IsAdminUser, ))
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


    def perform_create(self, serializer):
        if self.request.method == "OPTIONS":
            response = HttpResponse()
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
            response['Access-Control-Max-Age'] = 1000
            # note that '*' is not valid for Access-Control-Allow-Headers
            response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
            return response
        print('**********************************************************')
        serializer.save(data=self.request.POST)


    def create(self, request):
        print("*********************************************")
        if request.method == "OPTIONS":
            response = HttpResponse()
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
            response['Access-Control-Max-Age'] = 1000
            # note that '*' is not valid for Access-Control-Allow-Headers
            response['Access-Control-Allow-Headers'] = 'origin, x-csrftoken, content-type, accept'
            return response
        if request.method == "POST":
            print("*********************************************", request.POST)
            return super().create(request)

    def get_object(self):
        user_list = get_all_logged_in_users_ids()

        try:
            user_list.index(str(self.request.user.pk))
        except ValueError:
            raise NotAuthenticated

        abc = self.kwargs.get('pk')
        user = User.objects.filter(username=abc)
        user = user.first()
        if user is None:
            try:
                user = User.objects.get(pk=abc)
            except (ValueError, ObjectDoesNotExist):
                raise Http404
        return user


    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]




    '''
    @detail_route(methods=['get'])
    def date_list(self, request, pk=None):
        user = self.get_object()  # retrieve an object by pk provided
        username = self.request.Get.get('username', None)
        print('username', username)
        schedule = User.objects.filter(username=username)
        user_json = UserSerializer(user, many=True)
        return Response(user_json.data)

    @detail_route(methods=['post'], permission_classes=[IsAdminOrIsSelf], url_path='change-password')
        def set_password(self, request, pk=None):
    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get('user_id', None)
        username = self.request.query_params.get('username', None)
        print("))))))))))))))))))))))))))))))))))))))))))))")
        self.queryset = User.objects.filter(username=username)
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        query_set = User.objects.all()
        if username is not None:
            query_set = User.objects.filter(username=username)
        return query_set
    '''

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

