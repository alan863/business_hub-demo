from django.contrib.auth.models import User
from rest_framework import serializers
from .models import BlogPost
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import django.contrib.auth.hashers

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType




#content_type = ContentType.objects.get_for_model(User)
#permission = Permission.objects.create(
#   codename='can_see_vote_count',
#   name='Can See Vote Count',
#   content_type=content_type,
#)
'''
content_type = ContentType.objects.get_for_model(UserWithRoles)
addUserPermission = Permission.objects.get(
   codename='add_user',
   name = 'can add user', 
   content_type=content_type,
)

changeUserPermission = Permission.objects.get(
   codename='change_user',
   name = 'can change user', 
   content_type=content_type,
)

deleteUserPermission = Permission.objects.get(
   codename='delete_user',
   name = 'can delete user', 
   content_type=content_type,
)

viewUserPermission = Permission.objects.get(
   codename='view_user',
   name = 'can view user', 
   content_type=content_type,
)



admin_group, created = Group.objects.get_or_create(name='admin')

admin_group.permissions.set([addUserPermission,changeUserPermission, deleteUserPermission, viewUserPermission ])
partner_group, created = Group.objects.get_or_create(name='partner')
partner_group.permissions.set([ viewUserPermission])
client_group, created = Group.objects.get_or_create(name='client')
client_group.permissions.set([viewUserPermission])
'''


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['password'] = user.password
        # ...

        return token


class UserSerializer(serializers.ModelSerializer):
    

    
    #password = models.CharField(max_length=256)


    class Meta:
        model = UserWithRoles
        fields = ('id', 'username', 'password', 'first_name', 'last_name')
 
class BlogPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
 
    class Meta:
        model = BlogPost
        fields = ('id', 'user', 'date', 'body')


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ('id','roleName')