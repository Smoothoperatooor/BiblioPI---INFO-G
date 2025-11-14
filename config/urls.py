from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from app.views import *
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', views.LoginView, name='login'),
    path('cadastro/', views.CadastroView, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('forum/', ForumView.as_view(), name='forum'),
]

