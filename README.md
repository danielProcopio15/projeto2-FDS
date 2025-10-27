  <img width="597" height="330" alt="1_marcajc-27532970-removebg-preview" src="https://github.com/user-attachments/assets/bc8417f2-74d7-48a6-82fc-9a343c1d37a1" />


# Projeto NovoComm

portal reformulado é uma consultoria para aplicações web desenvolvida em **Django (Python)** que combina **notícias, gameficação e personalização** para engajar leitores.  
O projeto foi inspirado em metodologias ágeis e no uso de histórias do usuário para guiar o desenvolvimento.

---
##Ferramentas tecnológicas
- [Clickup](https://app.clickup.com/90132559199/v/l/6-901320778399-1): Utilizado para a gestão do nosso projeto
- HTML, CSS, Python, Django: Utilizados para o desenvolvimento Web
- [Figma](https://www.figma.com/design/CxJtSRKwt8lbcdUXEXBcZ7/Untitled?node-id=0-1&p=f&t=OUVp60PCG4ATGZiN-0): Utilizado para fazer o protótipo

---
## Funcionalidades Principais

- Login e cadastro com preferências de conteúdo, permitindo escolher temas de interesse e ocultar assuntos indesejados;

- Homepage personalizada, que se adapta automaticamente aos temas mais acessados;

- Navbar responsiva, fixa no topo e adaptável para diferentes dispositivos;

- Botão “Próxima Notícia”, que direciona para outras matérias do mesmo tema;

- Página “Para Você”, exibindo recomendações personalizadas com rolagem contínua;

- Botão “Resumo”, que apresenta tópicos curtos para leitura rápida e interação por hover.

---
## Demonstração do projeto

[Prototipagem](https://youtu.be/RADPIgk6zOA)
[Funcionalidades](https://youtu.be/i32FYrB3Jho)
[Teste estatísticas](https://www.youtube.com/watch?v=iVr5x6JALXE)
[Teste Login/Registro](https://youtu.be/dO_FzFLGr6w)



---
##Tela inicial

<img width="1902" height="944" alt="Captura de tela 2025-10-27 181518" src="https://github.com/user-attachments/assets/e77e30b6-a8a1-403e-8d2a-31190c25b411" />

---
##Tela da principal funcionalidade

<img width="957" height="909" alt="Captura de tela 2025-10-27 181845" src="https://github.com/user-attachments/assets/36f501f1-319d-4759-bb5e-6b3585303963" />

---

##Clickup

<img width="873" height="441" alt="Captura de tela 2025-10-27 185233" src="https://github.com/user-attachments/assets/659def33-2264-4219-b59a-42283288d738" />

[Clickup](https://app.clickup.com/90132559199/v/l/6-901320778399-1)

---
## Protótipo
<img width="1029" height="849" alt="image" src="https://github.com/user-attachments/assets/b70ba025-572d-4615-842f-1d17aeda6574" />
[Figma](https://www.figma.com/design/CxJtSRKwt8lbcdUXEXBcZ7/Untitled?node-id=0-1&p=f&t=OUVp60PCG4ATGZiN-0)

---
## Diagrama de atividades.

<img width="1759" height="944" alt="Captura de tela 2025-10-27 182107" src="https://github.com/user-attachments/assets/27c2639d-997c-4777-80ad-4afdede8efe0" />

[Miro](https://miro.com/app/board/uXjVJzod_qU=/)
---
## Issue tracker

[Issues/Bug tracker](https://github.com/danielProcopio15/projeto2-FDS/issues)

---
##Programação em pares]

Durante o desenvolvimento do projeto, estão sendo realizadas sessões de programação em par com o objetivo de revisar e aprimorar o código da aplicação. Essa prática colaborativa permite analisar diferentes partes do sistema de forma conjunta, identificar oportunidades de melhoria e corrigir erros de maneira mais eficiente. Como resultado, o código está se tornando mais consistente e o desenvolvimento, mais ágil e organizado.

<img width="1916" height="1028" alt="Captura de tela 2025-10-27 183255" src="https://github.com/user-attachments/assets/8ba74155-d87f-4ea5-a137-50de5785b0a5" /> 


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
## Equipe

- **Daniel Procópio** – Scrum Master | Desenvolvimento Backend (Django/Python) | Banco de Dados | Figma | https://www.linkedin.com/in/daniel-cunha-347006237/
- **Pedro Castro** – Product Owner | Desenvolvimento Frontend | Figma | UX/UI | https://www.linkedin.com/in/pedro-castro-94795a277/
- **Rafael Procópio** – Desenvolvimento Frontend & Backend | Banco de dados | Figma | https://www.linkedin.com/in/rafael-proc%C3%B3pio-75360a269/
- **Pedro Pinzón** – Desenvolvimento Backend | Banco de Dados |
- **Bernardo Santos** – Desenvolvimento Backend | Banco de Dados | https://www.linkedin.com/in/bernardo-santos-0b6761342/
- **Lucas Rocha** – Desenvolvimento Frontend & Backend | Design | https://www.linkedin.com/in/lucas-rocha-052a37364/
- **Mateus José** – Desenvolvimento Backend | Banco de Dados | https://www.linkedin.com/in/mateus-jos%C3%A9-48b4a6348/
- **Thiago Gabriel Tahim** - Desenvolvimento Frontend & Backend | Banco de dados |

---

## Contribuição

Pull requests são bem-vindos. Para mudanças maiores, abra primeiro uma *issue* para discussão.  

Certifique-se de atualizar os testes antes de enviar PR.  

---

## Licença

[MIT](https://choosealicense.com/licenses/mit/)
