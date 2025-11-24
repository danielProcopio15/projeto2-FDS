  <img width="597" height="330" alt="1_marcajc-27532970-removebg-preview" src="https://github.com/user-attachments/assets/bc8417f2-74d7-48a6-82fc-9a343c1d37a1" />


# Projeto NovoComm

O NovoComm é um portal de notícias reformulado desenvolvido em Django (Python). Ele atua como uma consultoria para aplicações web, combinando notícias, gamificação e personalização para aumentar o engajamento dos leitores.

O projeto foi construído sob a inspiração de metodologias ágeis, com o desenvolvimento guiado ativamente por histórias do usuário.
---

## 🛠️ Ferramentas tecnológicas

Para o desenvolvimento deste projeto, utilizamos as seguintes ferramentas:

- HTML, CSS, Python, Django, SqLite: Utilizados para o desenvolvimento Web, backend e dados.

- [ClickUp](https://app.clickup.com/90132559199/v/l/6-901320778399-1): Utilizado para a gestão ágil do nosso projeto.

- [Figma](https://www.figma.com/design/CxJtSRKwt8lbcdUXEXBcZ7/Untitled?node-id=0-1&p=f&t=OUVp60PCG4ATGZiN-0): Utilizado para a criação do protótipo e design.

---
## 🎯 Funcionalidades Principais

O sistema oferece diversas funcionalidades focadas na personalização e engajamento do leitor:

- Login e Cadastro Personalizado: Permite ao usuário escolher temas de interesse e ocultar assuntos indesejados.

- Homepage Adaptativa: A página inicial se adapta automaticamente, exibindo os temas mais acessados pelo usuário.

- Navbar Responsiva: Uma barra de navegação responsiva que se mantém fixa no topo da página.

- Botão “Próxima Notícia”: Direciona o leitor para outras matérias do mesmo tema, incentivando a navegação.

- Página “Para Você”: Exibe recomendações personalizadas em um formato de rolagem contínua.

- Botão “Resumo”: Apresenta tópicos curtos para leitura rápida e uma interação por hover.

---

## 🏞️ Demonstração do projeto

[Prototipagem](https://youtu.be/RADPIgk6zOA)

[Funcionalidades](https://youtu.be/i32FYrB3Jho)

[Teste estatísticas](https://www.youtube.com/watch?v=iVr5x6JALXE)

[Teste Login/Registro](https://youtu.be/dO_FzFLGr6w)



---

## 🧭 Tela inicial


<img width="1919" height="1079" alt="Captura de tela 2025-11-24 172556" src="https://github.com/user-attachments/assets/89f668e0-d059-4085-a2af-1f75bd1cc7a5" />


---

## 🕗 Clickup


<img width="873" height="441" alt="Captura de tela 2025-10-27 185233" src="https://github.com/user-attachments/assets/659def33-2264-4219-b59a-42283288d738" />


[Clickup](https://app.clickup.com/90132559199/v/l/6-901320778399-1)


---
## 🗺️ Diagrama de atividades.

<img width="1759" height="944" alt="Captura de tela 2025-10-27 182107" src="https://github.com/user-attachments/assets/27c2639d-997c-4777-80ad-4afdede8efe0" />

[Diagrama de atividades](https://miro.com/app/board/uXjVJzod_qU=/)

---
## 🔎 Issue e bugs tracker
  
[Issues/Bug tracker]([https://github.com/danielProcopio15/projeto2-FDS/issues](https://github.com/danielProcopio15/projeto2-FDS/issues?q=is%3Aissue%20state%3Aclosed%20no%3Alabel))

---
## 👥 Programação em pares

Durante o desenvolvimento do projeto, utilizamos a técnica de programação em pares, o que se provou essencial para a superação de desafios. Inicialmente, enfrentamos problemas de integração do CSS do layout original, sendo a Navbar o principal elemento em foco. No entanto, nossa colaboração também foi crucial para implementar as funcionalidades de Login e Cadastro. Ao trabalharmos juntos na lógica de autenticação e na interface de entrada de dados, conseguimos identificar e corrigir diversos erros estruturais e de segurança, resultando em um código mais limpo, robusto e com uma melhor experiência para o usuário.

(COLOCAR LINK PARA REGISTRO)

---

## 👨‍💻 Equipe

- [Daniel Procópio](https://www.linkedin.com/in/daniel-cunha-347006237/) – Scrum Master | Desenvolvimento Backend (Django/Python) | Banco de Dados | Figma |
- [Pedro Castro](https://www.linkedin.com/in/pedro-castro-94795a277/) – Product Owner | Desenvolvimento Frontend | Figma | UX/UI | https://www.linkedin.com/in/pedro-castro-94795a277/
- [Rafael Procópio](https://www.linkedin.com/in/rafael-proc%C3%B3pio-75360a269/) – Desenvolvimento Frontend & Backend | Banco de dados | Figma |
- **Pedro Pinzón** – Desenvolvimento Backend | Banco de Dados |
- [Bernardo Santos](https://www.linkedin.com/in/bernardo-santos-0b6761342/) – Desenvolvimento Backend | Banco de Dados |
- [Lucas Rocha](https://www.linkedin.com/in/lucas-rocha-052a37364/)– Desenvolvimento Frontend & Backend | Design |
- [Mateus José](https://www.linkedin.com/in/mateus-jos%C3%A9-48b4a6348/) – Desenvolvimento Backend | Banco de Dados |
- **Thiago Gabriel Tahim** - Desenvolvimento Frontend & Backend | Banco de dados |


---
## 💾 Instalação e uso

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


