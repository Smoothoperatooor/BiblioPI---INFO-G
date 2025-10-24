from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from app.views import *
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', views.LoginView, name='login'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('segunda/', SegundaView.as_view(), name='segunda'),
]

