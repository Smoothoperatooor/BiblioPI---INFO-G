from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib.auth.models import User


class IndexView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        categoria = request.GET.get('categoria', '')

        arquivos = Arquivo.objects.all()

        if query:
            arquivos = arquivos.filter(
                Q(nome__icontains=query) |
                Q(descricao__icontains=query) |
                Q(categoria__icontains=query)
            )

        if categoria:
            arquivos = arquivos.filter(categoria=categoria)

        context = {
            'arquivos': arquivos,
            'query': query,
            'categoria_selecionada': categoria,
            'categorias': Arquivo.CATEGORIAS,
        }

        # USUÁRIO É PROFESSOR?
        if request.user.is_authenticated:
            if hasattr(request.user, "usuario") and request.user.usuario.role == "professor":
                context['is_professor'] = True
                return render(request, 'professor/index.html', context)

        # caso contrário, é aluno
        context['is_professor'] = False
        return render(request, 'index.html', context)


class ForumView(View):
    def get(self, request, topico_id=None):
        topicos = Topico.objects.all()

        if topico_id is None:
            return render(request, "forum.html", {
                "topicos": topicos,
                "topico": None,
                "mensagens": None
            })

        topico = get_object_or_404(Topico, id=topico_id)
        mensagens = Mensagem.objects.filter(topico=topico).order_by("criado_em")

        return render(request, "forum.html", {
            "topicos": topicos,
            "topico": topico,
            "mensagens": mensagens
        })

    def post(self, request, topico_id=None):
        if not request.user.is_authenticated:
            return redirect("login")

        # se a URL não tiver /forum/<id>/ → erro 405
        if topico_id is None:
            return redirect("forum")

        topico = get_object_or_404(Topico, id=topico_id)
        texto = request.POST.get("texto", "").strip()

        if texto:
            Mensagem.objects.create(
                usuario=request.user,
                topico=topico,
                texto=texto
            )

        return redirect("forum", topico_id=topico.id)


class CriarTopicoView(View):
    def post(self, request):
        nome = request.POST.get("nome")
        desc = request.POST.get("desc")

        if nome and desc and request.user.is_authenticated:
            topico = Topico.objects.create(nome=nome, desc=desc)
            return redirect("forum", topico_id=topico.id)

        return redirect("forum")


class NovoArquivoView(View):
    def post(self, request, *args, **kwargs):
        nome = request.POST.get("nome")
        descricao = request.POST.get("descricao")
        categoria = request.POST.get("categoria")
        arquivo = request.POST.get("arquivo")  # CORRIGIDO: recebe arquivo via upload
        usuario=request.POST.get("user")
        
        Arquivo.objects.create(
            nome=nome,
            descricao=descricao,
            categoria=categoria,
            arquivo=arquivo,
            usuario=request.user
        )

        return redirect("index")

@login_required
def deletar_arquivo(request, arquivo_id):
    arquivo = get_object_or_404(Arquivo, id=arquivo_id)

    usuario_ext = request.user.usuario  

    # Professor pode deletar qualquer arquivo
    if usuario_ext.role == "professor":
        arquivo.delete()
        return render(request, "professor/index.html")

    # Aluno só apaga o que é dele
    if arquivo.usuario != request.user:
        return redirect("index")

    arquivo.delete()
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

    return render(request, "login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("index")


@login_required
def meu_perfil_view(request):
    user = request.user

    total_mensagens = Mensagem.objects.filter(usuario=user).count()
    total_arquivos = Arquivo.objects.filter(usuario=user).count()

    tempo_total = now() - user.date_joined
    dias_no_sistema = tempo_total.days
    horas_totais = int(tempo_total.total_seconds() // 3600)

    labels = ["Mensagens", "Arquivos", "Dias ativo"]
    data = [total_mensagens, total_arquivos, dias_no_sistema]

    context = {
        "total_mensagens": total_mensagens,
        "total_arquivos": total_arquivos,
        "dias_no_sistema": dias_no_sistema,
        "horas_totais": horas_totais,
        "labels": labels,
        "data": data,
    }

    return render(request, "meuperfil.html", context)
