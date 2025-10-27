  <img width="597" height="330" alt="1_marcajc-27532970-removebg-preview" src="https://github.com/user-attachments/assets/bc8417f2-74d7-48a6-82fc-9a343c1d37a1" />


# Projeto NovoComm

portal reformulado é uma consultoria para aplicações web desenvolvida em **Django (Python)** que combina **notícias, gameficação e personalização** para engajar leitores.  
O projeto foi inspirado em metodologias ágeis e no uso de histórias do usuário para guiar o desenvolvimento.

---

## Funcionalidades Principais

- Login e cadastro com preferências de conteúdo, permitindo escolher temas de interesse e ocultar assuntos indesejados;

- Homepage personalizada, que se adapta automaticamente aos temas mais acessados;

- Navbar responsiva, fixa no topo e adaptável para diferentes dispositivos;

- Botão “Próxima Notícia”, que direciona para outras matérias do mesmo tema;

- Página “Para Você”, exibindo recomendações personalizadas com rolagem contínua;

- Botão “Resumo”, que apresenta tópicos curtos para leitura rápida e interação por hover.
 

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

<img width="757" height="418" alt="Captura de tela 2025-10-13 191239" src="https://github.com/user-attachments/assets/a9711fad-cd92-4d2f-9395-9d1abf74877a" />
 

---

### Sprint

Sprint atual do grupo 

<img width="819" height="460" alt="Sem título" src="https://github.com/user-attachments/assets/6175932a-12f1-4e47-8dd6-cb6281f6b50f" />


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
