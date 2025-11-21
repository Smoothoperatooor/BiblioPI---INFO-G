from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout
from django.db.models import Q


class IndexView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')  # Parâmetro de busca
        categoria = request.GET.get('categoria', '')  # Filtro por categoria
        
        arquivos = Arquivo.objects.all()
        
        # Aplicar filtros de busca
        if query:
            arquivos = arquivos.filter(
                Q(nome__icontains=query) |
                Q(descricao__icontains=query) |
                Q(categoria__icontains=query)
            )
        
        # Filtro por categoria
        if categoria:
            arquivos = arquivos.filter(categoria=categoria)
        
        context = {
            'arquivos': arquivos,
            'query': query,
            'categoria_selecionada': categoria,
            'categorias': Arquivo.CATEGORIAS
        }
        return render(request, 'index.html', context)


class ForumView(View):
    def get(self, request, *args, **kwargs):
        topicos = Topico.objects.all()
        return render(request, 'forum.html', {
            'topicos': topicos,
            'chat_ativo': False  # importante
        })


def ChatView(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    mensagens = topico.mensagens.all().order_by("criado_em")

    # Se enviar mensagem
    if request.method == "POST":
        texto = request.POST.get("texto")
        if texto and request.user.is_authenticated:
            Mensagem.objects.create(
                topico=topico,
                usuario=request.user,
                texto=texto
            )
        return redirect("chat_topico", topico_id=topico_id)  # corrigido

    # Renderiza o chat dentro do layout do fórum
    return render(request, "forum.html", {
        "topico": topico,
        "mensagens": mensagens,
        "chat_ativo": True,               # ativa o container do chat
        "topicos": Topico.objects.all(),  # mantém a sidebar funcionando
    })


def CadastroView(request):
    if request.method == "POST": 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            login(request, form.save())
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "cadastro.html", { "form": form })


def LoginView(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.POST.get("next")
            if next_url:
                return redirect(next_url)

            return redirect("index")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", { "form": form })


def logout_view(request):
    if request.method == "POST": 
        logout(request) 
        return redirect("index")
