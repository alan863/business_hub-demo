from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
#from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .models import *
from . import serializers
from .serializers import *
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import authenticate
from .models import UserWithRoles
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth import logout 
from django.shortcuts import get_object_or_404

from .forms import *

def is_authenticated_admin(user): #authorization and authentication
        #return user.groups.filter(name='client').exists() 
    if not user.is_authenticated:
       
        return False
    print("USER AUTHENTICATED")
    
    if UserWithRoles.objects.filter(username=user.username,role=1).exists():
        print("USER AUTHORIZED")
        return True
    
    else:
        print("USER FAILED AUTHORIZATION")
        return False

def is_authenticated_client(user): #authorization and authentication
        #return user.groups.filter(name='client').exists() 
    if not user.is_authenticated:
       
        return False
    print("USER AUTHENTICATED")
    
    if UserWithRoles.objects.filter(username=user.username,role=3).exists() or UserWithRoles.objects.filter(username=user.username,role=1).exists():
        print("USER AUTHORIZED")
        return True
    
    else:
        print("USER FAILED AUTHORIZATION")
        return False


@user_passes_test(is_authenticated_client, login_url='/login/')
def index(request):
    return render(request, 'index.html')


# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            #form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']  
            print("username: "+username +"password:" +password+"firstname: "+first_name+"lastname: "+last_name)

            user = UserWithRoles(username = username, password = password, first_name = first_name, last_name = last_name)
            user.password = make_password(user.password)
            user.role = 3
            user.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


@user_passes_test(is_authenticated_admin, login_url='/login/?next=/ViewUserByID/')
def ViewUserByID(request):
    
    if request.method == 'POST':
        
        print("request: ")
       
        print(request.POST)
            
        id = request.POST.get('id')
        print("id from dropdown")
        print(id)

        
        users = UserWithRoles.objects.get(id=id)
        approved = request.POST.get('approved')
        if 'approved' in  request.POST and users.approved == False:
            users.approved=True
            users.save()
        
        print(users.approved)
        all = UserWithRoles.objects.all()
        ids = []
        for i in all:
            ids.append(i.id)
            print(i.id)
        context = {
        'ids': ids,
        'user' : users
        }
        print(context)
        return render(request, 'viewUsers.html', context)
    else: 
        #form = SearchUserForm()
         all = UserWithRoles.objects.all()
         ids = []
         for i in all:
            ids.append(i.id)
            print(i.id)
         context = {
            'ids': ids,
            }
         return render(request, 'viewUsers.html', context)        

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')





class SecureView(UserPassesTestMixin,AccessMixin,View):


    #@user_passes_test(is_client, login_url='/login/')
    #@action(detail=True, methods=['post','get'])
    def sec(self,request):
        #if not request.user.is_authenticated:
        #    print('login redirect')
        #    return redirect(f"/login/?next= {request.path}")
        #else:
            print('security passed')
            return render(request, 'index.html')
        

    def test_func(self):
        print('test func')
        return is_authenticated_client(self.request.user)
    #queryset = Roles.objects.all()
    login_url = '/login/'    
    permission_classes = [IsAuthenticatedOrReadOnly]


#class MyTokenObtainPairView(TokenObtainPairView):
#    serializer_class = serializers.MyTokenObtainPairSerializer


#PermissionRequiredMixin
#UserPassesTestMixin
class UserViewSet( viewsets.ModelViewSet):
    """
    Provides basic CRUD functions for the User model
    """
    
    #permission_required = 'webapp.add_user'
    #@user_passes_test(is_client)
    @action(detail=True, methods=['post'])
    def createUser(self, request, pk=None):
        #user = self.get_object()
        
        #some_salt = 'some_salt' 
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid(): #authorization and authentication check for demonstration
            user = UserWithRoles(username = request.data['username'],password = request.data['password'],first_name =  request.data['first_name'], last_name = request.data['last_name'])
            
            user.password = make_password(user.password)
            user.role = 3
            
            
            user.save()
            #client_group.user_set.add(user)
            print("user role: ")
            print(user.role) 
            #print(" user group is client: ")
            #print(user.groups.filter(name='client').exists())
            return HttpResponse("User with hashed password created in createUser() @action method")
        else:
            return HttpResponse("Invalid request")
        #UserViewSet.create(user,request,)
        #print("saved user in create()")
        
    

    login_url = '/login/'

    queryset = UserWithRoles.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
 
class BlogPostViewSet(viewsets.ModelViewSet):
    """
    Provides basic CRUD functions for the Blog Post model
    """
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]
 
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
#class RoleViewSet(viewsets.ModelViewSet):
#    queryset = Roles.objects.all()
#    serializer_class = RolesSerializer
#    permission_classes = [IsAuthenticatedOrReadOnly]