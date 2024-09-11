# tde-arquiteturadebancodeedados

Este é um programa simples em Python que simula um sistema de gerenciamento de músicas, playlists e reprodução. O sistema permite que o usuário se registre, faça login, crie playlists, adicione músicas, reproduza músicas e publique suas próprias músicas, transformando-se em um artista.

## Funcionalidades

- **Registrar Usuário**: Crie um novo usuário inserindo nome, email, senha e data de nascimento.
- **Login**: Faça login com as credenciais previamente cadastradas.
- **Ver Músicas**: Veja a lista de músicas disponíveis no banco de dados.
- **Buscar**: Busque músicas, gêneros e artistas.
- **Playlists**: Crie, visualize e gerencie playlists. Adicione músicas a uma playlist ou visualize músicas dentro de uma playlist.
- **Publicar Música**: Publique uma nova música. Se o usuário não for um artista, ele será automaticamente registrado como tal.

## Requisitos

- **Python 3.x**
- **SQLAlchemy** (ORM utilizado para interagir com o banco de dados)
- **SQLite** (ou outro banco de dados relacional suportado)

## Instalação e Execução

### Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/music_app.git
cd music_app
```

### Configurar o Ambiente Virtual

É recomendado criar um ambiente virtual para gerenciar as dependências do projeto.

#### No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Instalar Dependências

Com o ambiente virtual ativado, instale a biblioteca **SQLAlchemy**:

```bash
pip install sqlalchemy
```

### Executar o Programa

Após a instalação das dependências, execute o programa:

```bash
python main.py
```
