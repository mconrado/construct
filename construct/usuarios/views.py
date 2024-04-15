from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from rolepermissions.decorators import has_permission_decorator
from .models import Users
from django.urls import reverse
from django.contrib import auth
#Django Messages - definida lá no settings - MESSAGES_TAG
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.

@has_permission_decorator('cadastrar_vendedor')
def cadastrar_vendedor(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')        
        email = request.POST.get('email')
        password = request.POST.get('password')

        # TODO: Implementar validações dos dados.
        user = Users.objects.filter(email=email)

        if user.exists():
            # TODO: Utilizar messages do django
            messages.add_message(request, constants.ERROR, 'Já existe o usuário')
            return HttpResponse('Já existe o usuário')
            
        user = Users.objects.create_user(first_name=nome,last_name=sobrenome,username=email, email=email, password=password, cargo="V")
        # TODO: Utilizar messages do django para redirecionar com uma mensagem
        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')
        return redirect(reverse('cadastrar_vendedor'))
        #return HttpResponse('Conta do usuário criada')
    else:
        vendedores = Users.objects.filter(cargo="V")
        return render(request,'cadastrar_vendedor.html', {'vendedores':vendedores})

@has_permission_decorator('cadastrar_vendedor')
def excluir_usuario(request, id):
    vendedor = get_object_or_404(Users, id=id)
    vendedor.delete()
    messages.add_message(request, constants.ERROR, 'Vendedor excluído com sucesso!')
    return redirect(reverse('cadastrar_vendedor'))

def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('plataforma'))
        return render(request,'login.html')
    elif request.method =="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(username=email, password=password)

        if not user:
            #TODO: Redirecionar com mensagem de erro
            messages.add_message(request, constants.ERROR, 'Usuário inválido!')
            return HttpResponse('Usuário inválido!')
        else:
            auth.login(request,user)
            messages.add_message(request, constants.SUCCESS, 'Usuário logado com sucesso!')
            return HttpResponse('Usuário logado com sucesso')

def logout(request):
    request.session.flush()
    return redirect(reverse('login'))
