  <img width="597" height="330" alt="1_marcajc-27532970-removebg-preview" src="https://github.com/user-attachments/assets/bc8417f2-74d7-48a6-82fc-9a343c1d37a1" />


# Projeto NovoComm

portal reformulado é uma consultoria para aplicações web desenvolvida em **Django (Python)** que combina **notícias, gameficação e personalização** para engajar leitores.  
O projeto foi inspirado em metodologias ágeis e no uso de histórias do usuário para guiar o desenvolvimento.

---

## Funcionalidades Principais

### Sistema de login e cadastro com preferências de conteúdo.
Usuários podem criar contas, escolher temas de interesse e ocultar assuntos que não desejam consumir.

### Personalização de homepage via cache e comportamento de navegação.
A página inicial adapta-se às categorias mais acessadas, priorizando conteúdos de interesse do leitor.

### Divisões temáticas com identidade visual por seção.
Cada área do portal (Esportes, Política, Cultura etc.) possui cores e estilos próprios para facilitar a identificação.

### Navbar responsiva e chamativa.
Barra de navegação fixa no topo com cores da marca JC, tornando-se menu sanduíche em telas menores.

### Botão “Próxima Notícia”.
Permite avançar para outra matéria do mesmo tema sem precisar voltar à página inicial.

### Layout otimizado de leitura e anúncios.
Substitui anúncios intrusivos por cards de matérias relacionadas, mantendo propagandas laterais e experiência limpa.

### Página “Para Você”.
Sessão personalizada com rolagem contínua, mostrando notícias e recomendações baseadas no histórico do usuário.

### Botão “Resumo” nas matérias.
Exibe um quadro com tópicos curtos da notícia para leitura rápida, com interação hover em imagens.

### Gamificação da experiência.
Usuários ganham pontos e selos (Bronze, Prata, Ouro) por ler, comentar e compartilhar notícias, com mensagens de incentivo.

### Sistema de estatísticas de uso.
Registra acessos e temas mais lidos, permitindo análises e recomendações personalizadas 

---
## Protótipo
<img width="1029" height="849" alt="image" src="https://github.com/user-attachments/assets/b70ba025-572d-4615-842f-1d17aeda6574" />

---
## Diagrama de atividades.

representação dos caminhos, decisões e interações do usuário.

<img width="1915" height="1015" alt="Captura_de_tela_2025-09-22_165846" src="https://github.com/user-attachments/assets/2cfeb7e9-dc94-436c-9bf3-9dcd75cfd3bd" />

---
## Screen Cast

https://youtu.be/RADPIgk6zOA

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

<img width="1827" height="553" alt="Captura de tela 2025-09-22 211431" src="https://github.com/user-attachments/assets/1d880975-bcbb-4bba-a317-c3ecdd0369e8" />


 ## Descrição das histórias
 
# 🧾 Histórias de Usuário

As histórias de usuário foram criadas com base nas necessidades do **Sistema Jornal do Commercio (SJCC)**, seguindo a estrutura dos **3Cs (Cartão, Conversa e Confirmação)**, de forma clara e voltada à entrega de valor.

---

##  História 1 — Login

**Como usuário,**  
quero poder fazer login com meu e-mail e senha,  
**para** acessar o portal com minhas preferências de conteúdo salvas.

**Principais pontos:**
- Interface simples com campos de usuário e senha.  
- Mensagens de erro claras (usuário não encontrado ou senha incorreta).  
- Validação de login conectada ao banco de dados.  

---

##  História 2 — Cadastro

**Como novo usuário,**  
quero criar uma conta e escolher os temas que me interessam,  
**para** receber notícias personalizadas e ocultar assuntos que não gosto.

**Principais pontos:**
- Validação de e-mail e senha fortes.  
- Preferências e temas salvos no banco de dados.  
- Layout com caixas de texto e botões simples e intuitivos.  

---

##  História 3 — Divisões de Conteúdo

**Como leitor,**  
quero visualizar as seções do site bem organizadas,  
**para** entender facilmente em qual área de conteúdo estou.

**Principais pontos:**
- Criação de “divs” e “sections” por tema (esportes, política, cultura etc).  
- Cores de fundo correspondentes ao tema (ex: verde para esportes).  
- Layout flexível com display grid ou flex.  

---

##  História 4 — Navbar

**Como usuário,**  
quero uma barra de navegação fixa e chamativa,  
**para** acessar rapidamente as seções do portal.

**Principais pontos:**
- Navbar vermelha no topo com identidade visual do JC.  
- Links para todas as áreas principais.  
- Torna-se menu sanduíche em telas menores.  

---

##  História 5 — Botão “Próxima Notícia”

**Como leitor,**  
quero acessar outra notícia do mesmo tema rapidamente,  
**para** continuar lendo sem precisar voltar à página inicial.

**Principais pontos:**
- Botão no canto superior direito com prévia da próxima notícia.  
- Sempre redireciona para uma nova matéria do mesmo tema.  

---

##  História 6 — Ajuste de Layout de Notícia e Anúncios

**Como leitor,**  
quero ver matérias relacionadas ao artigo que estou lendo,  
**para** continuar navegando sem distrações e com menos anúncios no meio do texto.

**Principais pontos:**
- Seção de artigos relacionados no meio da página.  
- Anúncios movidos para a lateral (sticky, alternando em blocos).  
- Layout em cards pequenos e responsivos.  

---

##  História 7 — Página “Para Você”

**Como usuário,**  
quero ter uma página personalizada com notícias que gosto,  
**para** encontrar meus conteúdos preferidos em um só lugar.

**Principais pontos:**
- Aba “Para Você” na navbar.  
- Página com rolagem contínua e base em interesses do usuário.  
- Sugestões de matérias semelhantes ao final da página.  

---

##  História 8 — Botão “Resumo”

**Como usuário com pouco tempo,**  
quero acessar um resumo rápido das notícias,  
**para** entender o conteúdo sem precisar ler tudo.

**Principais pontos:**
- Botão “Resumo” no início da matéria.  
- Exibe uma box com até 8 tópicos curtos.  
- Efeito hover nas imagens mostrando breves descrições.  

---

##  História 9 — Personalização com Cache

**Como usuário frequente,**  
quero que o site me mostre notícias baseadas no que mais leio,  
**para** encontrar rapidamente conteúdos do meu interesse.

**Principais pontos:**
- Registro das visitas e categorias acessadas pelo usuário.  
- Homepage personalizada com base nesse histórico.  
- Uso de cache para manter desempenho e carregamento rápido.  

---

##  História 10 — Gamificação da Experiência

**Como usuário do portal,**  
quero ganhar pontos e selos conforme interajo com as notícias,  
**para** me sentir motivado a continuar navegando e lendo mais.

**Principais pontos:**
- Pontuação por ações (ler, comentar, compartilhar, visitar).  
- Exibição de nível e selo (Bronze, Prata, Ouro).  
- Mensagens de incentivo ao subir de nível.  


---

### Sprint

Definição da primeira codificação do grupo 

<img width="1340" height="492" alt="image" src="https://github.com/user-attachments/assets/37ca50f2-08f4-4b6b-8626-fc4c67c4e17b" />

---

### Issue tracker

<img width="1851" height="922" alt="image" src="https://github.com/user-attachments/assets/1746fdc8-b59e-429a-b616-ae831460acb0" />

---


###prototipação de baixa fidelidade AxB
#### prototipação A
<img width="1025" height="823" alt="image" src="https://github.com/user-attachments/assets/b6aba58d-4447-4bb9-9dd1-c0dcaf50e0e2" />

[link para o wireframe](https://www.figma.com/design/CxJtSRKwt8lbcdUXEXBcZ7/Untitled?node-id=0-1&p=f&t=nnFXSY9vHAmyp73j-0)





## Papéis no Time

- **PO (Product Owner):** responsável por priorizar histórias.  
- **Dev Backend (Python/Django):** lógica, APIs e banco de dados.  
- **Dev Frontend (HTML/CSS/JS):** interface e usabilidade.  
- **Design UX/UI:** experiência do usuário e identidade visual.  
- **Scrum Master:** garante a execução do processo ágil.  

---

## Integrantes do Grupo

- **Daniel Procópio** – Scrum Master | Desenvolvimento Backend (Django/Python) | Banco de Dados | Figma | https://www.linkedin.com/in/daniel-cunha-347006237/
- **Pedro Castro** – Product Owner | Desenvolvimento Frontend | Figma | UX/UI | https://www.linkedin.com/in/pedro-castro-94795a277/
- **Rafael Procópio** – Desenvolvimento Frontend & Backend | Figma | https://www.linkedin.com/in/rafael-proc%C3%B3pio-75360a269/
- **Pedro Pinzón** – Desenvolvimento Backend | Banco de Dados |
- **Bernardo Santos** – Desenvolvimento Backend | Banco de Dados | https://www.linkedin.com/in/bernardo-santos-0b6761342/
- **Lucas Rocha** – Desenvolvimento Frontend & Backend | Design | https://www.linkedin.com/in/lucas-rocha-052a37364/
- **Mateus José** – Desenvolvimento Backend | Banco de Dados | https://www.linkedin.com/in/mateus-jos%C3%A9-48b4a6348/


---

## Contribuição

Pull requests são bem-vindos. Para mudanças maiores, abra primeiro uma *issue* para discussão.  

Certifique-se de atualizar os testes antes de enviar PR.  

---

## Licença

[MIT](https://choosealicense.com/licenses/mit/)
