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
    def get(self, request, topico_id=None):
        topicos = Topico.objects.all()
        if topico_id is None:
            return render(request, "forum.html", {"topicos": topicos, "topico": None, "mensagens": None})
        topico = get_object_or_404(Topico, id=topico_id)
        mensagens = Mensagem.objects.filter(topico=topico).order_by("criado_em")
        return render(request, "forum.html", {"topicos": topicos, "topico": topico, "mensagens": mensagens})

    def post(self, request, topico_id=None):
        # evita POST se usuário não autenticado
        if not request.user.is_authenticated:
            return redirect("login")

        # precisa do topico_id para salvar a mensagem
        if topico_id is None:
            return redirect("forum")  # ou onde fizer sentido

        topico = get_object_or_404(Topico, id=topico_id)
        texto = request.POST.get("texto", "").strip()
        if texto:
            Mensagem.objects.create(usuario=request.user, topico=topico, texto=texto)

        return redirect("forum", topico_id=topico.id)
    
class CriarTopicoView(View):
    def post(self, request):
        nome = request.POST.get("nome")
        desc = request.POST.get("desc")

        if nome and desc and request.user.is_authenticated:
            topico = Topico.objects.create(
                nome=nome,
                desc=desc,
            )
            return redirect("forum", topico_id=topico.id)

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
