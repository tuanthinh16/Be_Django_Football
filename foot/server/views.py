from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, UserDTOSerializer, AccountDTOSerializer, UserSerializer
from rest_framework import generics, permissions
from knox.models import AuthToken
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth.models import User
import json
from django.http import JsonResponse



class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        serializers = AccountDTOSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        user = serializer.validated_data['user']
        if user:
            login(request, user)

        return super(LoginAPI, self).post(request, format=None)


@api_view(['GET'])
def getAllAccount(request):
    account = User.objects.all()
    serializers = UserDTOSerializer(account, many = True)
    return Response(serializers.data)

@api_view(['GET'])
def getProfile(request,usr):
    try:
        account = User.objects.filter(username = usr).values()
        serializers = UserSerializer(account,many = True)

        return Response(serializers.data)
    except:
        return JsonResponse({'error': 'User not found'}, status=404)
    
@api_view(['GET'])
def getHistory(request,usr):
    listTime = []
    id = getid(usr)
    try:
        tokens = AuthToken.objects.filter(user_id=id).values()
        for token in tokens:
            listTime.append(token)
        return JsonResponse({'data':listTime}) 
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

def getid(user):
    user = User.objects.filter(username = user).first()
    return user.id

@api_view(['POST'])
def updateProfile(request,usr):
    try:
        account = User.objects.filter(username=usr).first()
        account.first_name = request.POST.get('first_name')
        account.last_name = request.POST.get('last_name')
        account.save()
        return JsonResponse({'data':account.value})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)