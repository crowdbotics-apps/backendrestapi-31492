from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet, ReadOnlyModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions, status
from subscriptions.models import Plan, Subscription
from apps.models import App
from users.models import User

from home.api.v1.serializers import (
    SignupSerializer,
    UserSerializer,
    PlanSerializer,
    SubscriptionSerializer,
    AppSerializer,
)


class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})

class PlanViewSet(ReadOnlyModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

def get_user_from_request(request):
    key = request.META.get('HTTP_AUTHORIZATION')
    # print(key)
    # print(type(key))

    if key:
        keyTok = key.split()
        # print(keyTok)
        # print(keyTok[1])
        tokenObj = Token.objects.get(key=keyTok[1])
        user = tokenObj.user.id
    else:
        user = request.user.id
    return user


class SubscriptionViewSet(ModelViewSet):

    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # subs = Subscription.objects.filter(user=self.request.user)
        subs = Subscription.objects.all()
        return subs

    def list(self, request, *args, **kwargs):
        try:
            usr = get_user_from_request(request)
            subs = Subscription.objects.filter(user=usr)
            # subs = Subscription.objects.filter(user=request.user)
            serializer = SubscriptionSerializer(subs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error' : e.args}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            usr = get_user_from_request(request)
            # subs = Subscription.objects.filter(user=request.user, id=kwargs['pk'])
            subs = Subscription.objects.filter(user=usr, id=kwargs['pk'])
            serializer = SubscriptionSerializer(subs, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception as e:
            return Response({'error' : e.args}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            usr = get_user_from_request(request)
            if  usr != int(request.data['user']):
                return Response({'error', 'Operation not allowed'},
                                status=status.HTTP_401_UNAUTHORIZED)
            subs = Subscription()
            serializer = SubscriptionSerializer(subs, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error' : e.args}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            usr = get_user_from_request(request)

            # if request.user.id != request.data['user']:
            if  usr != int(request.data['user']):
                return Response({'error', 'Operation not allowed'},
                         status=status.HTTP_401_UNAUTHORIZED)

            subs = Subscription.objects.get(user=usr, id=kwargs['pk'])
            # subs = Subscription.objects.get(user=request.user, id=kwargs['pk'])
            serializer = SubscriptionSerializer(subs, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error' : e.args}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            usr = get_user_from_request(request)
            if 'user' in request.data and usr != int(request.data['user']):
                    return Response({'error', 'Operation not allowed'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            subs = Subscription.objects.get(user=usr, id=kwargs['pk'])
            # subs = Subscription.objects.get(user=request.user, id=kwargs['pk'])
            serializer = SubscriptionSerializer(subs, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error' : e.args}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class AppViewSet(ModelViewSet):

    queryset = App.objects.all()
    serializer_class = AppSerializer

    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            usr = get_user_from_request(request)
            apps = App.objects.filter(user=usr)
            # apps = App.objects.filter(user=request.user)
            serializer = AppSerializer(apps, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error' : e.args}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            usr = get_user_from_request(request)
            apps = App.objects.filter(user=usr, id=kwargs['pk'])
            # apps = App.objects.filter(user=request.user, id=kwargs['pk'])
            serializer = AppSerializer(apps, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error' : e}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            usr = get_user_from_request(request)            
            if usr != int(request.data['user']):
                return Response({'error', 'Operation not allowed'},
                                status=status.HTTP_401_UNAUTHORIZED)
            subs = App()
            serializer = AppSerializer(subs, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error' : e.args}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            usr = get_user_from_request(request)
            if  usr != int(request.data['user']):
                return Response({'error', 'Operation not allowed'},
                                status=status.HTTP_401_UNAUTHORIZED)
            apps = App.objects.get(user=usr, id=kwargs['pk'])
            # apps = App.objects.get(user=request.user, id=kwargs['pk'])
            serializer = AppSerializer(apps, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error' : e.args}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            usr = get_user_from_request(request)
            if 'user' in request.data and usr != int(request.data['user']):
                return Response({'error', 'Operation not allowed'},
                                status=status.HTTP_401_UNAUTHORIZED)

            subs = App.objects.get(user=usr, id=kwargs['pk'])
            # subs = App.objects.get(user=request.user, id=kwargs['pk'])
            serializer = AppSerializer(subs, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error' : e.args}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        # Should all associated subscription set to inactive?
        try:
            usr = get_user_from_request(request)
            apps = App.objects.filter(user=usr, id=kwargs['pk'])
            # apps = App.objects.filter(user=request.user, id=kwargs['pk'])
            apps.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error' : e.args}, status=status.HTTP_400_BAD_REQUEST)