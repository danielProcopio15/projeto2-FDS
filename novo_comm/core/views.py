from django.shortcuts import render, redirect 
from django.contrib.auth.models import User 
from django.contrib import messages
import re 
from django.contrib.auth import authenticate, login as auth_login

def home(request):
    return render(request, 'core/home.html')

def cadastro(request):
    context = {}
    
    if request.method == 'POST':
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repetir_senha = request.POST.get('repetir_senha')
        
        # Define os valores preenchidos para serem passados de volta ao template
        # A senha NUNCA é retornada para o template por segurança.
        context['username_value'] = username
        context['email_value'] = email
        
        #VALIDAÇÃO DE OBRIGATORIEDADE E SENHAS IGUAIS
        if not all([username, email, password, repetir_senha]):
            messages.error(request, 'Preencha todos os campos.')
            return render(request, 'core/cadastro.html', context)
            
        if password != repetir_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'core/cadastro.html', context)
            
        #VALIDAÇÃO DE EMAIL
        if '@' not in email or not email.lower().endswith('.com'):
            messages.error(request, 'Email inválido (deve conter @ e terminar com .com).')
            return render(request, 'core/cadastro.html', context)
            
        #VALIDAÇÃO DE SENHA
        if len(password) < 6:
            messages.error(request, 'A senha deve ter no mínimo 6 dígitos.')
            return render(request, 'core/cadastro.html', context)
            
        if not re.search(r'\d', password):
            messages.error(request, 'A senha deve conter pelo menos 1 número.')
            return render(request, 'core/cadastro.html', context)
            
        if not re.search(r'[A-Z]', password):
            messages.error(request, 'A senha deve conter pelo menos 1 letra maiúscula.')
            return render(request, 'core/cadastro.html', context)
            
        #VALIDAÇÃO DE UNICIDADE
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe.')
            return render(request, 'core/cadastro.html', context)
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return render(request, 'core/cadastro.html', context)
            
        #5. CRIAÇÃO E SALVAMENTO DO USUÁRIO
        try:
            User.objects.create_user(
                username=username, 
                email=email, 
                password=password
            )
            
            # Limpa o contexto antes de redirecionar para não carregar dados desnecessários
            messages.success(request, 'Cadastro realizado com sucesso! Você pode fazer o login.')
            return redirect('login') 
            
        except Exception as e:
            messages.error(request, 'Erro interno ao cadastrar. Tente novamente.')
            return render(request, 'core/cadastro.html', context) # Retorna com os dados
            
    # Se a requisição for GET (primeiro acesso), retorna o template vazio
    return render(request, 'core/cadastro.html', {})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Variável para armazenar o username que tentaremos autenticar
        username_to_auth = None
        
        # 1. Tenta buscar o usuário pelo email
        try:
            user = User.objects.get(email=email)
            username_to_auth = user.username
        except User.DoesNotExist:
            # Se o email não for encontrado, definimos um username que não existe.
            # Isso é crucial para que o 'authenticate' falhe, mas o erro seja tratado
            # de forma unificada no bloco 'else'.
            username_to_auth = 'nonexistent_user_for_security_check'
            
        # 2. Tenta autenticar usando o username e a senha
        # Se username_to_auth for o valor dummy, esta função retornará None.
        user = authenticate(request, username=username_to_auth, password=password)
        
        if user is not None:
            # Autenticação bem-sucedida
            auth_login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')
        else:
            # Falha de autenticação (email inexistente OU senha incorreta)
            # Exibe a mensagem genérica que você solicitou.
            messages.error(request, 'Usuário ou senha errada.') 
            
            # Retorna o valor do email preenchido para o template, 
            # melhorando a experiência do usuário.
            context = {'email_value': email}
            return render(request, 'core/login.html', context)
            
    # Se a requisição for GET (primeiro acesso)
    return render(request, 'core/login.html')