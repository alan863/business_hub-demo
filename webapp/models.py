from enum import Enum
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
 
class RoleChoices (Enum):
 admin = 1,
 partner = 2,
 client = 3



class UserWithRoles(User):
     
      
      ROLE_CHOICES = (
          (RoleChoices.admin, 'admin'),
          (RoleChoices.partner, 'partner'),
          (RoleChoices.client, 'client'),
      )
      role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
      approved = models.BooleanField(default=False)
    

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(
        default=timezone.now
    )
    body = models.CharField(default='', max_length=200)
 
    def __str__(self):
        return self.body
    
class Roles(models.Model):
    roleName = models.CharField(default='', max_length=200)
 
    def __str__(self):
        return self.body

#class RolesAndUsers(models.Model):
