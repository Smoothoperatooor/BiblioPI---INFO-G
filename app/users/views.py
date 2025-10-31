from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout


def CadastroView(request):
    if request.method == "POST": 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            login(request, form.save())
    else:
        form = UserCreationForm()
    return render(request, 'users/cadastro.html', { "form": form })

def LoginView(request): 
    if request.method == "POST": 
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): 
            login(request, form.get_user())
    else: 
        form = AuthenticationForm()
    return render(request, 'users/login.html', { "form": form })