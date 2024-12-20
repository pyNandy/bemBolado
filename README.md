
# Projeto Integrador Transdisciplinar em Sistemas de Informação II
Este projeto é um sistema funcional desenvolvido como parte do trabalho de conclusão de curso de Sistemas de Informação na Universidade Cruzeiro do Sul. 
Ele simula um ambiente de mercado real, destacando a importância da interdisciplinaridade no desenvolvimento de soluções tecnológicas. 
A Pizzaria Bem Bolado, criada exclusivamente para fins educacionais, serve como base para esta plataforma.

Projetada para oferecer uma navegação intuitiva, um sistema de pedidos eficiente e uma gestão integrada dos processos de uma pizzaria delivery, 
a plataforma proporciona uma experiência realística de mercado, reforçando a importância da interdisciplinaridade no desenvolvimento de soluções tecnológicas.

## Linguagem e Ferramentas Utilizadas

- **Linguagem de Programação:** Python
- **Framework:** Django


## Habilidades Desenvolvidas

- Uso de CSS, HTML e JavaScript para posicionamento de elementos, display grid, flex, hover, entre outros.
- Desenvolvimento de um projeto responsivo com menu hambúrguer para telas menores, implementado com JavaScript.



## Funcionalidades

- O sistema possui um menu superior para navegação, permitindo que o usuário acesse cada sessão de produtos.
- Oferece uma navegação intuitiva, um sistema de pedidos eficiente e uma gestão integrada dos processos de uma pizzaria delivery.

## Pré-requisitos

- Python 3.8+
- Django 3.2+

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    ```

2. Crie e ative o ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Realize as migrações do banco de dados:
    ```bash
    python manage.py migrate
    ```

5. Execute o servidor de desenvolvimento:
    ```bash
    python manage.py runserver
    ```

## Configuração

- Configure as variáveis de ambiente no arquivo `.env`.

## Uso

- Acesse o sistema em `http://127.0.0.1:8000/` e navegue pelas funcionalidades disponíveis.

## Arquitetura do Sistema

- Estrutura de diretórios:

    ```
Projeto Integrador
│   loja
│    └──asgi.py
│    └──forms.py
│    └──models.py
│    └──settings.py
│    └──urls.py
│    └──wsgi.py
│    
├── media/
│   └── produto_imagens/
│
├── notificar/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── consumers.py
│   ├── routing.py
│   ├── notifications.py
│   ├── urls.py
│   └── views.py
│
├── pedido/
│   ├── templates/pedido/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── perfil/
│   ├── templates/perfil/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── produto/
│   ├── templates/produto/
│   ├── templatetags/
│   ├── admin.py
│   ├── apps.py
│   ├── carrinho.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── admin/
│   ├── parciais/
│   ├── registration/
│   └── static/
│        └── assets/
│            └── custom/
│                └── css/ 
│                └── js/   
├── utils/
│   ├── validacpf.py/
│   └── utils.py
│
├── venv/
├──.gitignore
├──README.md
├──manage.py
└──db.sqlite3

    ```

## Contribuição

1. Fork este repositório.
2. Crie uma branch com a nova feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Add nova feature'`).
4. Push para a branch (`git push origin feature/nova-feature`).
5. Crie um novo Pull Request.

## Testes

- Para executar os testes, utilize:
    ```bash
    python manage.py test
    ```

## Licença

Este projeto está licenciado sob os termos da licença MIT.

## Autor

- Ernane Oliveira (nandy.eso@gmail.com)

## Contato

- Para dúvidas ou suporte, entre em contato [48 99615-9805](nandy.eso@gmail.com).
