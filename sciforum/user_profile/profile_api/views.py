from .serializers import ProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, status #, pagination
from post.models import Post
from user_profile.models import ProfileViewerInfo, Profile, UserEmployment, UserEducation, UserLanguages\
    , UserContact, UserSkills
from .serializers import UserSerializer, CustomUserSerializer, JWTSerializer, UserEmploymentSerializer\
    , UserEducationSerializer, UserLanguageSerializer, UserSkillsSerializer, UserContactSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
# from django.contrib.auth.mixins import LoginRequiredMixin
from rest_auth.views import LoginView
# from rest_auth.registration.views import RegisterView, SocialLoginView
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt import authentication
from .utils import get_client_ip
from django.db.models import Count, Sum
from .mixins import GetSerializerClassMixin


class ProfileViewSet(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['aboutMe', 'user']


# views for users
class UserViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):

    '''
        here it describes the way of getting user information over the drf depending on the serializer.
    '''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_action_classes = {
        'list': CustomUserSerializer,
    }


class UserListView(ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(methods=['get'], detail=True, url_path='retrieve_by_username/(?P<username>\w+)')
    def retrieve_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class UserDetailView(RetrieveAPIView):
    # authentication_classes = [authentication.JSONWebTokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    # serializer_class = UserSerializer
    lookup_field = 'username'

    def get_serializer_class(self):
        # print(self.request.session.get('_auth_user_id', 0))
        # print(self.kwargs['username'])
        user = self.request.user
        if user.is_authenticated and user.username == self.kwargs['username']:
            return UserSerializer
        return CustomUserSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        profileViewCount = 0
        totalPostViewCount = 0
        agent_info = ''
        requestUser = ''

        try:
            profileViewCount = ProfileViewerInfo.objects.filter(user=user).values('user').annotate(viewCount=Count('viwer_ip', distinct=True))[0]['viewCount']
        except Exception as exep:
            print(exep)

        # print(profileViewCount)

        try:
            agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255]
        except Exception as exep:
            print(exep)

        try:
            requestUser = request.user
        except Exception as exep:
            print(exep)

        try:
            totalPostViewCount = Post.objects.filter(owner=self.get_object()).aggregate(totalPostViewCount=Sum('viewCount'))['totalPostViewCount']
        except Exception as exep:
            print(exep)

        #print(totalPostViewCount)
        profileObj = Profile.objects.get(user=self.get_object())
        profileObj.postViews = totalPostViewCount
        profileObj.save(update_fields=('postViews', ))

        newProfileViewer = ProfileViewerInfo(user=self.get_object(), viewerUsername=requestUser, visitDate=now(), viwer_ip=get_client_ip(request), viwer_agent_info=agent_info)
        newProfileViewer.save()

        return super().retrieve(request, *args, **kwargs)


    '''
    @action(methods=['get'], detail=True, url_path='retrieve_by_username/(?P<username>\w+)')
    def retrieve_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    '''


class UserUpdateView(UpdateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


# User Credentials
class UserEmploymentFilter(FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='iexact')

    class Meta:
        model = UserEmployment
        fields = ('username',)


class UserEmploymentViewSet(viewsets.ModelViewSet):
    queryset = UserEmployment.objects.all()
    serializer_class = UserEmploymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserEmploymentFilter
    # filterset_fields = ['user__username']
    http_method_names = ['get']

    '''def get_queryset(self):
        """
        filtering against a `username` query parameter in the URL.
        """
        queryset = UserEmployment.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user__username=username)
        return queryset'''


class UserEmploymentEditViewSet(viewsets.ModelViewSet):

    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = UserEmployment.objects.all()
    serializer_class = UserEmploymentSerializer

    http_method_names = ['get', 'post', 'patch', 'put', 'delete']


class UserEducationFilter(FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='iexact')

    class Meta:
        model = UserEducation
        fields = ('username',)


class UserEducationViewSet(viewsets.ModelViewSet):

    queryset = UserEducation.objects.all()
    serializer_class = UserEducationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserEducationFilter

    http_method_names = ['get']


class UserEducationEditViewSet(viewsets.ModelViewSet):

    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = UserEducation.objects.all()
    serializer_class = UserEducationSerializer

    http_method_names = ['get', 'post', 'patch', 'put', 'delete']


class UserLanguagesFilter(FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='iexact')

    class Meta:
        model = UserLanguages
        fields = ('username',)


class UserLanguagesViewSet(viewsets.ModelViewSet):

    queryset = UserLanguages.objects.all()
    serializer_class = UserLanguageSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = UserLanguagesFilter

    http_method_names = ['get']


class UserLanguagesEditViewSet(viewsets.ModelViewSet):

    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = UserLanguages.objects.all()
    serializer_class = UserLanguageSerializer

    http_method_names = ['get', 'post', 'patch', 'put', 'delete']


class UserSkillsFilter(FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='iexact')

    class Meta:
        model = UserSkills
        fields = ('username',)


class UserSkillsViewSet(viewsets.ModelViewSet):
    queryset = UserSkills.objects.all()
    serializer_class = UserSkillsSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = UserSkillsFilter

    http_method_names = ['get']


class UserSkillsEditViewSet(viewsets.ModelViewSet):

    # authentication_classes = [authentication.JSONWebTokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    queryset = UserSkills.objects.all()
    serializer_class = UserSkillsSerializer

    http_method_names = ['get', 'post', 'patch', 'put', 'delete']


class UserContactFilter(FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='iexact')

    class Meta:
        model = UserSkills
        fields = ('username',)


class UserContactViewSet(viewsets.ModelViewSet):
    queryset = UserContact.objects.all()
    serializer_class = UserContactSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = UserContactFilter

    http_method_names = ['get']


class UserContactEditViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = UserContact.objects.all()
    serializer_class = UserContactSerializer

    http_method_names = ['get', 'post', 'patch', 'put', 'delete']


# views for authentication
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        '''try:
            request_user, data = request.get_parameters(request)
            user = request.get_user_by_username(data['username'])
            update_last_login(None, user)
        except Exception as exc:
            return None'''

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })


# JWT Views
class JWTLoginView(ObtainJSONWebToken):
    serializer_class = JWTSerializer


class JWTRegisterView(RegisterView):
    # serializer_class = JWTSerializer

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        # token, created = Token.objects.get_or_create(user=user)

        Profile.objects.update_or_create(user=user)  # creating user profile when the user is registered

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        jwttoken = jwt_encode_handler(payload)

        return Response({
            'token': jwttoken,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        })


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def get_response(self):
        # get_adapter(self.request).login(self.request, self.user)

        Profile.objects.update_or_create(user=self.user)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        user = self.user

        payload = jwt_payload_handler(user)
        jwttoken = jwt_encode_handler(payload)

        return Response({
            'token': jwttoken,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })


class CustomLoginView(LoginView):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        Profile.objects.filter(pk=user).update(lastAccessDate=now())
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })


class CustomRegisterView(RegisterView):

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })

