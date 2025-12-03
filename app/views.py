from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, logout
from django.db.models import Q #SERVE PARA O FILTRO
from django.utils.timezone import now
from django.contrib.auth.models import User


class IndexView(View):
    def get(self, request, *args, **kwargs):
        filtro = request.GET.get('valcate', '')
        categoria = request.GET.get('categoria', '')

        arquivos = Arquivo.objects.all()

        if filtro:
            arquivos = arquivos.filter(
                Q(nome__icontains=filtro) |
                Q(descricao__icontains=filtro) |
                Q(categoria__icontains=filtro)
            )

        if categoria:
            arquivos = arquivos.filter(categoria=categoria)

        context = {
            'arquivos': arquivos,
            'filtro': filtro,
            'categoria_selecionada': categoria,
            'categorias': Arquivo.CATEGORIAS,
        }

    
        return render(request, "index.html", context)

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

        topico = Topico.objects.create(nome=nome, desc=desc)
        return redirect("forum", topico_id=topico.id)


class NovoArquivoView(View):
    def post(self, request, *args, **kwargs):
        nome = request.POST.get("nome")
        descricao = request.POST.get("descricao")
        categoria = request.POST.get("categoria")
        arquivo = request.POST.get("arquivo") 
        usuario = request.POST.get("user")
        
        Arquivo.objects.create(
            nome=nome,
            descricao=descricao,
            categoria=categoria,
            arquivo=arquivo,
            usuario=request.user
        )

        return redirect("index")
    
class CadastroView(View):
    def get(self, request):
        return render(request, "cadastro.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        funcao = request.POST['funcao']

        user = User.objects.create_user(username=username, password=password)
        Usuario.objects.create(user=user, funcao=funcao)

        return redirect("login")
    

def MeuPerfilView(request):
    user = request.user

    total_mensagens = Mensagem.objects.filter(usuario=user).count()
    total_arquivos = Arquivo.objects.filter(usuario=user).count()

    # SISTEMA DE NÍVEL
    if total_mensagens >= 50:
        nivel = "Lendário"
    elif total_mensagens >= 20:
        nivel = "Veterano"
    elif total_mensagens >= 5:
        nivel = "Iniciante"
    else:
        nivel = None

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
        "nivel": nivel, 
    }

    return render(request, "meuperfil.html", context)


def DeletarTrabalho(request, arquivo_id):
    arquivo = get_object_or_404(Arquivo, id=arquivo_id)
 

    arquivo.delete()
    return redirect("index")


def DeletarTopico(request, topico_id):
    topico = get_object_or_404(Topico, id=topico_id)
    
   
    topico.delete()
    return redirect("forumLista") 


def LoginView(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("index")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def LogoutView(request):
    if request.method == "POST":
        logout(request)
        return redirect("index")



