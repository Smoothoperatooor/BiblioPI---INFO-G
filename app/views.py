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
        # Check user role
        is_professor = False
        if request.user.is_authenticated:
            try:
                if request.user.usuario.role == "professor":
                    is_professor = True
                    return render(request, 'professor/indexPRO.html', context)
            except:
                pass  # in case user has no Usuario record

        # Search
        query = request.GET.get('q', '')
        categoria = request.GET.get('categoria', '')

        arquivos = Arquivo.objects.all()

        # Filter by query
        if query:
            arquivos = arquivos.filter(
                Q(nome__icontains=query) |
                Q(descricao__icontains=query) |
                Q(categoria__icontains=query)
            )

        # Filter by category
        if categoria:
            arquivos = arquivos.filter(categoria=categoria)

        context = {
            'arquivos': arquivos,
            'query': query,
            'categoria_selecionada': categoria,
            'categorias': Arquivo.CATEGORIAS,
            'is_professor': is_professor,
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

class NovoArquivoView(View):
    def post(self, request, *args, **kwargs):
        nome = request.POST.get("nome")
        descricao = request.POST.get("descricao")
        categoria = request.POST.get("categoria")
        arquivo = request.POST.get("arquivo")

        Arquivo.objects.create(
            nome=nome,
            descricao=descricao,
            categoria=categoria,
            arquivo=arquivo
        )

        return redirect("index")
        
class CadastroView(View):
    def get(self, request):
        return render(request, "cadastro.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(username=username, password=password)

        Usuario.objects.create(user=user, role=role)

        return redirect("login")

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
