from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import copy
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from . import models
from . import forms
import utils

class BasePerfil(View):
    template_name = 'perfil/criar.html'
    
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        self.perfil = None
        if self.request.user.is_authenticated:
            self.perfil = models.Perfil.objects.filter(
                usuario=self.request.user
            ).first()
            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil
                )
            }
        else:
            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None
                )
            }
        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']
        self.renderizar = render(
            self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar

class Criar(BasePerfil):
    template_name = 'perfil/register.html'

    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            messages.error(
                self.request,
                'Existem erros no formulário de cadastro. Verifique se todos '
                'os campos foram preenchidos corretamente.'
            )
            return self.renderizar

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        # Adicionando logs para verificar nome e sobrenome
        print(f'Nome: {first_name}, Sobrenome: {last_name}')
        
        # Usuário logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(
                User, username=self.request.user.username)
            usuario.username = username
            if password:
                usuario.set_password(password)
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()
            if not self.perfil:
                self.perfilform.cleaned_data['usuario'] = usuario
                print(self.perfilform.cleaned_data)
                perfil = models.Perfil(**self.perfilform.cleaned_data)
                perfil.save()
            else:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()
        # Usuário não logado (novo)
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()
            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()
        
        if password:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password
            )
            if autentica:
                login(self.request, user=usuario)
        
        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        messages.success(
            self.request,
            'Seu cadastro foi criado ou atualizado com sucesso.'
        )
        messages.success(
            self.request,
            'Você fez login e pode concluir sua compra.'
        )
        return redirect('produto:carrinho')

class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')

class Login(View):
    template_name = 'perfil/login.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        if not username or not password:
            messages.error(self.request, 'Usuário ou senha inválidos.')
            return redirect('perfil:login')

        usuario = authenticate(self.request, username=username, password=password)
        if not usuario:
            messages.error(self.request, 'Usuário ou senha inválidos.')
            return redirect('perfil:login')

        login(self.request, user=usuario)
        messages.success(self.request, 'Você fez login no sistema e pode concluir sua compra.')
        return redirect('produto:carrinho')

class Logout(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))
        logout(self.request)
        self.request.session['carrinho'] = carrinho
        self.request.session.save()
        return redirect('produto:lista')

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Seu dados foram atualizado com sucesso!')
            return redirect('profile')  # Ajuste conforme necessário
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'p_form': p_form
    }
    return render(request, 'profile/profile.html', context)
