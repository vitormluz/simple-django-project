from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_
from django.contrib.auth.models import User
from .forms import ContatoForm, ProdutosModelForm
from .models import Produtos


def index(request):
    context = {
        'produtos': Produtos.objects.all()
    }

    return render(request, 'core/index.html', context)


def contato(request):
    form = ContatoForm(request.POST or None)

    if str(request.method) == 'POST':
        if form.is_valid():

            form.send_mail()
            messages.success(request, 'E-Mail enviado com sucesso.')
            form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar o e-mail.')

    context = {
        'form': form
    }

    return render(request, 'core/contato.html', context)

def cadastro(request):
    if request.method != 'POST':
        return render(request, 'core/cadastro.html')
    
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')

    user = User.objects.filter(username=username).first()

    if user:
        messages.error(request, 'Esse usuário já existe, escolha outro nome')
        return render(request, 'core/cadastro.html')

    if not username or not email or not password or not password2:
        messages.error(request, 'Complete todos os campos requiridos.')
        return render(request, 'core/cadastro.html')

    if password != password2:
        messages.error(request, 'As senhas precisam estar iguais.')
        return render(request, 'core/cadastro.html')

    if len(password) < 8:
        messages.error(request, 'A senha precisa ter no mínimo 8 caracteres.')
        return render(request, 'core/cadastro.html')

    if len(username) < 6:
        messages.error(request, 'O username precisa ter no mínimo 6 caracteres.')
        return render(request, 'core/cadastro.html')
    
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    
    messages.success(request, 'Usuário cadastrado com sucesso!')
    return redirect('login')


def login(request):
    if request.method != 'POST':
        return render(request, 'core/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user:
        login_(request, user)

        messages.success(request, 'Logado com sucesso.')
        return redirect('produto')
    else:
        messages.error(request, 'Username ou senha inválidos.')
        return render(request, 'core/login.html')


def produto(request):
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            form = ProdutosModelForm(request.POST, request.FILES)
            if form.is_valid():

                form.save()
                messages.success(request, 'Produto salvo com sucesso.')
                form = ProdutosModelForm()
            else:
                messages.error(request, 'Erro ao salvar produto.')
        else:
            form = ProdutosModelForm()
        
        context = {
            'form': form
        }

        return render(request, 'core/produto.html', context)
    else:
        messages.error(request, 'Você deve estar logado para publicar algum produto')
        return redirect('login')

