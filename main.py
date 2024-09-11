# Importações necessárias
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

# Base do SQLAlchemy
Base = declarative_base()

# Modelos do banco de dados

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String)
    data_nascimento = Column(String)
    is_artista = Column(Boolean, default=False)
    playlists = relationship('Playlist', back_populates='usuario')

class Artista(Base):
    __tablename__ = 'artistas'
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    descricao = Column(String)
    usuario = relationship('Usuario')

class Playlist(Base):
    __tablename__ = 'playlists'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(String)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship('Usuario', back_populates='playlists')
    musicas = relationship('Contem', back_populates='playlist')

class Musica(Base):
    __tablename__ = 'musicas'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    id_artista = Column(Integer, ForeignKey('artistas.id'))
    id_genero = Column(Integer, ForeignKey('generos.id'))
    data_lancamento = Column(DateTime)
    duracao = Column(Integer)
    reproducoes = Column(Integer, default=0)
    playlist_associada = relationship('Contem', back_populates='musica')

class Genero(Base):
    __tablename__ = 'generos'
    id = Column(Integer, primary_key=True)
    nome = Column(String)

class Contem(Base):
    __tablename__ = 'contem'
    id_playlist = Column(Integer, ForeignKey('playlists.id'), primary_key=True)
    id_musica = Column(Integer, ForeignKey('musicas.id'), primary_key=True)
    playlist = relationship('Playlist', back_populates='musicas')
    musica = relationship('Musica', back_populates='playlist_associada')

class Reproduz(Base):
    __tablename__ = 'reproduz'
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    id_musica = Column(Integer, ForeignKey('musicas.id'))
    data_reproducao = Column(DateTime, default=datetime.datetime.now)

# Configuração da base de dados
engine = create_engine('sqlite:///musica.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Funções auxiliares
def ascii_menu(text, options):
    print(text)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = input("Escolha uma opção: ")
    return int(choice)

# Função para adicionar músicas e gêneros prontos
def adicionar_musicas_e_generos_prontos():
    generos_existentes = session.query(Genero).all()
    if not generos_existentes:
        generos = ["Rock", "Pop", "Jazz", "Eletrônica", "Clássica"]
        for g in generos:
            session.add(Genero(nome=g))
        session.commit()

    musicas_existentes = session.query(Musica).all()
    if not musicas_existentes:
        rock = session.query(Genero).filter_by(nome="Rock").first().id
        pop = session.query(Genero).filter_by(nome="Pop").first().id
        jazz = session.query(Genero).filter_by(nome="Jazz").first().id
        # Criação de músicas fictícias sem artistas por enquanto
        musicas = [
            Musica(nome="Bohemian Rhapsody", id_genero=rock, data_lancamento=datetime.datetime(1975, 10, 31), duracao=360),
            Musica(nome="Billie Jean", id_genero=pop, data_lancamento=datetime.datetime(1982, 11, 30), duracao=300),
            Musica(nome="Take Five", id_genero=jazz, data_lancamento=datetime.datetime(1959, 9, 21), duracao=320)
        ]
        session.add_all(musicas)
        session.commit()

# Tela de login e registro
def tela_login_registro():
    adicionar_musicas_e_generos_prontos()  # Adiciona músicas e gêneros prontos ao iniciar
    opcao = ascii_menu("Bem-vindo ao sistema de música!", ["Registrar", "Logar"])
    if opcao == 1:
        registrar()
    elif opcao == 2:
        logar()

# Registro de novo usuário
def registrar():
    nome = input("Digite seu nome: ")
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")
    data_nascimento = input("Digite sua data de nascimento: ")
    novo_usuario = Usuario(nome=nome, email=email, senha=senha, data_nascimento=data_nascimento)
    session.add(novo_usuario)
    session.commit()
    print("Registro completo! Logando agora...")
    usuario_pagina_inicial(novo_usuario)

# Login do usuário existente
def logar():
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")
    usuario = session.query(Usuario).filter_by(email=email, senha=senha).first()
    if usuario:
        print("Login bem-sucedido!")
        usuario_pagina_inicial(usuario)
    else:
        print("Usuário não encontrado ou senha incorreta.")
        tela_login_registro()

# Página inicial do usuário
def usuario_pagina_inicial(usuario):
    while True:
        opcao = ascii_menu(f"Bem-vindo, {usuario.nome}!", ["Ver músicas", "Buscar", "Ver minhas playlists", "Publicar uma música"])
        if opcao == 1:
            ver_musicas(usuario)
        elif opcao == 2:
            buscar(usuario)
        elif opcao == 3:
            ver_playlists(usuario)
        elif opcao == 4:
            publicar_musica(usuario)

# Ver músicas disponíveis no banco de dados
def ver_musicas(usuario):
    musicas = session.query(Musica).all()
    for i, musica in enumerate(musicas, 1):
        print(f"{i}. {musica.nome}")
    opcao = input("Escolha uma música para reproduzir ou salvar em uma playlist, ou 'v' para voltar: ")
    if opcao != 'v':
        musica_escolhida = musicas[int(opcao) - 1]
        opcao_musica(usuario, musica_escolhida)

# Ver playlists do usuário
def ver_playlists(usuario):
    playlists = session.query(Playlist).filter_by(id_usuario=usuario.id).all()
    if playlists:
        print("Suas playlists:")
        for i, playlist in enumerate(playlists, 1):
            print(f"{i}. {playlist.nome}")
            opcao = input("Escolha uma playlist para ver suas músicas, 'c' para criar uma nova ou 'v' para voltar: ")
            if opcao == 'c':
                criar_playlist(usuario)
            elif opcao != 'v':
                playlist_escolhida = playlists[int(opcao) - 1]
                ver_musicas_da_playlist(playlist_escolhida)
    else:
        print("Você não tem nenhuma playlist. Criando nova playlist...")
        criar_playlist(usuario)

# Ver músicas dentro de uma playlist
def ver_musicas_da_playlist(playlist):
    print(f"Músicas na playlist {playlist.nome}:")
    if playlist.musicas:
        for contem in playlist.musicas:
            print(f"- {contem.musica.nome}")
    else:
        print("A playlist está vazia.")
    input("Pressione qualquer tecla para voltar à página inicial...")

# Opção para uma música
def opcao_musica(usuario, musica):
    opcao = ascii_menu(f"Música: {musica.nome}", ["Reproduzir", "Salvar em uma playlist", "Voltar"])
    if opcao == 1:
        reproduzir_musica(usuario, musica)
    elif opcao == 2:
        salvar_na_playlist(usuario, musica)
    elif opcao == 3:
        usuario_pagina_inicial(usuario)

# Reproduzir música
def reproduzir_musica(usuario, musica):
    reproduz = Reproduz(id_usuario=usuario.id, id_musica=musica.id)
    session.add(reproduz)
    session.commit()
    print(f"Você está ouvindo {musica.nome}!")

# Salvar música em uma playlist
def salvar_na_playlist(usuario, musica):
    playlists = session.query(Playlist).filter_by(id_usuario=usuario.id).all()
    if playlists:
        for i, playlist in enumerate(playlists, 1):
            print(f"{i}. {playlist.nome}")
        opcao = input("Escolha uma playlist ou 'n' para criar uma nova: ")
        if opcao == 'n':
            criar_playlist(usuario, musica)
        else:
            playlist_escolhida = playlists[int(opcao) - 1]
            adicionar_musica_a_playlist(playlist_escolhida, musica)
    else:
        print("Nenhuma playlist encontrada. Criando nova playlist...")
        criar_playlist(usuario, musica)

def adicionar_musica_a_playlist(playlist, musica):
    contem = Contem(id_playlist=playlist.id, id_musica=musica.id)
    session.add(contem)
    session.commit()
    print(f"Música {musica.nome} adicionada à playlist {playlist.nome}!")

# Criar uma nova playlist
def criar_playlist(usuario, musica=None):
    nome = input("Digite o nome da playlist: ")
    descricao = input("Digite uma descrição para a playlist: ")
    nova_playlist = Playlist(nome=nome, descricao=descricao, id_usuario=usuario.id)
    session.add(nova_playlist)
    session.commit()
    print(f"Playlist {nome} criada com sucesso!")
    if musica:
        adicionar_musica_a_playlist(nova_playlist, musica)

# Função de busca
def buscar(usuario):
    termo = input("Digite o termo de busca: ").lower()
    musicas = session.query(Musica).filter(Musica.nome.ilike(f"%{termo}%")).all()
    artistas = session.query(Artista).join(Usuario).filter(Usuario.nome.ilike(f"%{termo}%")).all()
    generos = session.query(Genero).filter(Genero.nome.ilike(f"%{termo}%")).all()

    print("Resultados de músicas:")
    for musica in musicas:
        print(musica.nome)
    
    print("Resultados de artistas:")
    for artista in artistas:
        print(artista.usuario.nome)
    
    print("Resultados de gêneros:")
    for genero in generos:
        print(genero.nome)

    escolha = input("Escolha uma música, ou digite 'v' para voltar: ")
    if escolha != 'v':
        musica_escolhida = musicas[int(escolha) - 1]
        opcao_musica(usuario, musica_escolhida)

# Publicar uma música
def publicar_musica(usuario):
    if not usuario.is_artista:
        print("Você ainda não é um artista. Vamos te registrar como um!")
        descricao = input("Digite uma descrição ou biografia: ")
        novo_artista = Artista(id_usuario=usuario.id, descricao=descricao)
        usuario.is_artista = True
        session.add(novo_artista)
        session.commit()
    nome = input("Nome da música: ")
    
    # Exibir opções de gêneros ao invés de inserir o id
    generos = session.query(Genero).all()
    for i, genero in enumerate(generos, 1):
        print(f"{i}. {genero.nome}")
    id_genero = generos[int(input("Escolha o gênero da música: ")) - 1].id
    
    data_lancamento = datetime.datetime.now()
    nova_musica = Musica(nome=nome, id_artista=usuario.id, id_genero=id_genero, data_lancamento=data_lancamento, duracao=200)
    session.add(nova_musica)
    session.commit()
    print(f"Música {nome} publicada com sucesso!")

# Inicializar o sistema
if __name__ == "__main__":
    tela_login_registro()
