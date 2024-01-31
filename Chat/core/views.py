from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import RegisterSerializer , ListUserSerializer , UserConfirmEmailSerializer
from rest_framework.views import APIView
from .models import User
from django.db.models import Q
from rest_framework import status , permissions
from django.shortcuts import render


@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    return Response({
        'user_info':{
            'id': user.id,
            'username':user.username,
            'first_name':user.first_name,
            'last_name':user.last_name,
        },
        'token':{token}
    })

def login(request):
    if(request.method == "GET"):
        return render(request, "core/login.html")

@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
class ListUser(APIView):
    permission_classes= [permissions.IsAuthenticated]
    
    def get(self , request):
        users = User.objects.filter(~Q(pk=request.user.pk)).filter(is_superuser=False)
        serializer = ListUserSerializer(users , many=True)
        return Response(serializer.data,status.HTTP_200_OK)

def user_list(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'core/user_list.html', {'users': users})

def signup(request):
    return render(request , 'core/register.html')

class UserConfirmEmailView(APIView):
    serializer_class = UserConfirmEmailSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=kwargs)
        if not serializer.is_valid():
            return render(request, 'core/error_confirming.html')
        return render(request, 'core/confirmed.html')