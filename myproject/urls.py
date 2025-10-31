from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from . import views
from django.conf.urls.static import static 
from django.conf import settings 
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/', views.CadastroView, name="cadastro"),
    path('login/', views.LoginView, name="login"),
]

