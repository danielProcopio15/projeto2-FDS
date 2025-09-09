# portal reformulado

portal reformulado é uma consultoria para aplicações web desenvolvida em **Django (Python)** que combina **notícias, gameficação e personalização** para engajar leitores.  
O projeto foi inspirado em metodologias ágeis e no uso de histórias do usuário para guiar o desenvolvimento.

---

## Funcionalidades Principais
- Gameficação com palavras cruzadas e quizzes baseados em notícias.  
- Sistema de pontos e ranking entre usuários.  
- Perfil de usuário com personalização de interesses.  
- Página inicial minimalista e adaptada ao comportamento do leitor.  
- Enquetes no final das matérias para participação da comunidade.  
- Navegação sequencial estilo TikTok.  
- Integração com parceiros para troca de pontos por descontos.  
- Versão em áudio/vídeo das manchetes e resumos.  

---

## Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/newsportal-gamificado.git
cd newsportal-gamificado
pip install -r requirements.txt
```

Crie o banco de dados e execute as migrações:

```bash
python manage.py migrate
```

Crie um superusuário para acessar o painel administrativo:

```bash
python manage.py createsuperuser
```

Inicie o servidor local:

```bash
python manage.py runserver
```

Acesse em: [http://localhost:8000](http://localhost:8000)

---

## Uso

Exemplo de como rodar a aplicação localmente e explorar funcionalidades:

```python
# Executar servidor
python manage.py runserver

# Acessar rotas principais:
# / -> Página inicial personalizada
# /games -> Jogos e quizzes baseados em notícias
# /profile -> Configuração de interesses do usuário
# /ranking -> Ranking de pontos
```

---

## Histórias do Usuário

As principais histórias do usuário que guiaram o desenvolvimento (seguindo os **3Cs**: claras, concisas e com entrega de valor):

1. Como **leitor interessado em esportes**, quero jogar palavras cruzadas baseadas nas notícias lidas, para fixar o conteúdo de forma divertida.  
2. Como **usuário ativo**, quero acumular pontos por interações, para trocar por recompensas ou subir no ranking.  
3. Como **novo usuário**, quero selecionar meus interesses no cadastro, para receber notícias personalizadas.  
4. Como **usuário recorrente**, quero editar meus interesses, para ajustar minha experiência.  
5. Como **usuário que valoriza praticidade**, quero deslizar entre notícias no estilo TikTok, para consumir conteúdo rapidamente.  
6. Como **usuário engajado**, quero comentar nas notícias, para compartilhar opiniões e debater.  
7. Como **usuário que preza pela clareza**, quero uma home limpa, para encontrar notícias sem distrações.  
8. Como **usuário assíduo**, quero trocar pontos por descontos de empresas parceiras, para ter benefícios reais.  
9. Como **leitor curioso**, quero responder enquetes no fim das matérias, para expressar minha opinião.  
10. Como **usuário em transporte**, quero ouvir as manchetes em áudio, para acompanhar sem precisar ler.  

---

## Backlog

Backlog representado no estilo **Kanban (Jira)**:

<img width="1086" height="709" alt="image" src="https://github.com/user-attachments/assets/5ef76432-0bdf-4281-8c4f-15947ca9e345" />


---

## Papéis no Time

- **PO (Product Owner):** responsável por priorizar histórias.  
- **Dev Backend (Python/Django):** lógica, APIs e banco de dados.  
- **Dev Frontend (HTML/CSS/JS):** interface e usabilidade.  
- **Design UX/UI:** experiência do usuário e identidade visual.  
- **Scrum Master:** garante a execução do processo ágil.  

---

## Integrantes do Grupo

- **Daniel Procópio** – Scrum Master | Desenvolvimento Backend (Django/Python) | Banco de Dados | Figma  
- **Pedro Castro** – Product Owner | Desenvolvimento Frontend | Figma | UX/UI  
- **Rafael Procópio** – Desenvolvimento Frontend & Backend | Figma  
- **Pedro Pinzón** – Desenvolvimento Backend | Banco de Dados  
- **Bernardo Santos** – Desenvolvimento Backend | Banco de Dados  
- **Lucas Rocha** – Desenvolvimento Frontend & Backend | Design  
- **Mateus José** – Desenvolvimento Backend | Banco de Dados  

---

## Contribuição

Pull requests são bem-vindos. Para mudanças maiores, abra primeiro uma *issue* para discussão.  

Certifique-se de atualizar os testes antes de enviar PR.  

---

## Licença

[MIT](https://choosealicense.com/licenses/mit/)
