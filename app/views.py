from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login

class IndexView(View):
    def get(self, request, *args, **kwargs):
        arquivos = Arquivo.objects.all()
        return render(request, 'index.html' , {'arquivos':arquivos})
    def post(self, request):
        pass

class SegundaView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'segunda.html')
    def post(self, request):
        pass


class CadastroView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cadastro.html')
    def post(self, request):
        pass
    
def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # ou o nome da sua página inicial
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return render(request, 'login.html')  # renderiza de novo o form com erro

    # se for GET, exibe o formulário normalmente
    return render(request, 'login.html')