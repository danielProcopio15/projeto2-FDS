  <img width="597" height="330" alt="1_marcajc-27532970-removebg-preview" src="https://github.com/user-attachments/assets/bc8417f2-74d7-48a6-82fc-9a343c1d37a1" />


# Projeto NovoComm

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

<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/7ae22ad0-5821-48fa-9bbd-90638f19fe14" />


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
 
1. Priorize separar cada uma das áreas de interesse em “divs” ou “Sections” em que nessas divisões haja uma cor predominante que combine com o tema, como por exemplo: A sessão de esportes deve ter um fundo verde como cor principal. Utilize o display grid ou flex.
2. Reestruturar listagens de matérias em cards minimalistas que estejam dentro das divs e das sections. Mudar (imagem, título, categoria). 2 formatos - 1o em grade 3x2    2o em tiras (1 noticia por lina/setor
3. Criem uma nav bar chamativa(com cor vermelha e fonte de letra compatível com a identidade do JC) que esteja no “header” da página, ela deve ter links diretos para cada uma das áreas de interesse como política, esportes e etc.  
4. Façam uma outra aba dentro da página do JC em que as notícias sejam exibidas em formato scrollavel com notícias baseadas no interesse do usuário. O acesso a esta aba deve estar na nav bar com um nome com cor e fonte chamativa.
5. Substituir os anúncios que ficam NO MEIO das notícias por uma seção limpa com pelo menos 1 ou mais artigos relacionados (titulo curto, link e Layout em cards pequenos alinhados em grid responsivo.). Os anúncios devem ficar na parte lateral da página para não atrapalhar a experiência do usuários. Layout em cards pequenos alinhados em grid responsivo. Os anúncios devem acompanhar um pedaço da página até certo ponto, dando espaço para outro anúncio, imagens ou continuidade de notícias.As notícias devem estar centralizadas, com espaço para as propagandas. as boxes estarão em formato de grid, mas ao entrar na notícia, estará escrita por extenso no meio.
6. Criem um sistema de avaliação simples, apenas colocando a quantidade de estrelas que o usuário deseja colocar(1 até 5), no final de cada notícia, algo simples, no canto inferior direito da tela.  
7. Criem um botão ao início da notícia, com o nome “resumo”, que ao clica-lo, abre um quadrado, uma box, com os tópicos pertinentes da matéria. A box deve conter no máximo 8 tópicos com 2 linhas cada, no máximo( a box deve se ajustar a quantidade de conteúdo).  
8. Criem um botão com uma prévia da notícia no canto superior direito, com poucos elementos, para clicar e redirecionar para outra notícia. Esse botão deve permanecer, sempre jogando para uma notícia nova. 
9. Criem um dado estatístico por meio de visitações do user à página(visitação do controller) e entregue na página principal notícias destinadas ao user.
10. Façam com que dentro da navbar, apareça uma opção de jogos com base em notícias disponíveis no portal de notícias. Ao estagnar em um quizz ou minigame, o user recebe a opção no canto inferior do jogo para “receber uma dica”, que ao clicar redireciona para um anúncio que gera a resposta do joguinho.

---

### Sprint

Definição da primeira codificação do grupo 

<img width="1340" height="492" alt="image" src="https://github.com/user-attachments/assets/37ca50f2-08f4-4b6b-8626-fc4c67c4e17b" />


---
### Diagrama de atividades.

representação dos caminhos, decisões e interações do usuário.

<img width="1915" height="1015" alt="Captura_de_tela_2025-09-22_165846" src="https://github.com/user-attachments/assets/2cfeb7e9-dc94-436c-9bf3-9dcd75cfd3bd" />






---

### Issue tracker

<img width="1851" height="922" alt="image" src="https://github.com/user-attachments/assets/1746fdc8-b59e-429a-b616-ae831460acb0" />

---


###prototipação de baixa fidelidade AxB
#### prototipação A
<img width="1025" height="823" alt="image" src="https://github.com/user-attachments/assets/b6aba58d-4447-4bb9-9dd1-c0dcaf50e0e2" />

#### prototipação B
<img width="1029" height="849" alt="image" src="https://github.com/user-attachments/assets/d2599348-53f1-40d1-bf74-73f2332e849a" />

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
