from django.urls import path
from django.urls import path, include
from rest_framework import routers
from django.contrib.auth import views as auth_views

from . import views
 
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', views.BlogPostViewSet)
router.register(r'users', views.UserViewSet)
#router.register(r'secure',views.SecureViewSet)
#router.register(r'login')
#router.register(r'roles', views.RoleViewSet)

#secRouter = routers.DefaultRouter(trailing_slash=False)
#secRouter.register(r'sec',views.SecureViewSet)
urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'', views.index, name='index'),
    #path(r'', include("django.contrib.auth.urls")),
    path(r'secure/', views.SecureView.as_view()),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('ViewUserByID/', views.ViewUserByID, name='ViewUserByID'),
]

