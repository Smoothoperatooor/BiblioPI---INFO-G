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

