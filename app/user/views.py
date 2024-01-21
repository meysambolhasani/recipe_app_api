from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthtokenSerilizer


class CreateUserView(generics.CreateAPIView):
    """ Create new user """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for user """

    serializer_class = AuthtokenSerilizer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
