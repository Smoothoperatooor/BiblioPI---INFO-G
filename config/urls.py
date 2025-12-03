from django.contrib import admin
from django.urls import path
from app.views import *
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #INDEX
    path('', IndexView.as_view(), name='index'),
    path('novoArquivo/', NovoArquivoView.as_view(), name="novoArquivo"),
    path('arquivo/<int:arquivo_id>/deletar/', views.DeletarTrabalho, name='deletarArquivo'),

    #LOGIN E CADASTRO
    path('login/', views.LoginView, name='login'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('logout/', views.LogoutView, name='logout'),

    #FÓRUM
    path('forum/', ForumView.as_view(), name='forumLista'),
    path('forum/<int:topico_id>/', ForumView.as_view(), name="forum"),
    path('forum/novoTopico/', views.CriarTopicoView.as_view(), name="novoTopico"),
    path('topico/<int:topico_id>/deletar/', views.DeletarTopico, name='deletarTopico'),

    #MEUPERFIL
    path("meuperfil/", views.MeuPerfilView, name="meuPerfil"),
]

