from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

conx_str = 'mysql+mysqlconnector://root:@localhost:3306/task_list'
engine = create_engine(conx_str, echo=True)

BaseModel = declarative_base()

class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    
    def __repr__(self):
        return f'<User'
    
# Criando tabelas (Se não existirem).
BaseModel.metadata.create_all(bind=engine)

#Interagindo com banco de dados
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)

#Abrindo conexão
session = SessionLocal()

#Operações com o banco de dados aqui

#Criando um usuário
# user = User(
#     username="davi",
#     password="123"
# )
# session.add(user)
# session.commit()
# #Criando um usuário
# user = User(
#     username="heric1",
#     password="123"
# )
# session.add(user)
# session.commit()

# #buscar com condição
# users = session.query(User).all()
# print(users)

# user = session.query(User).filter(User.username == "davi").first()
# user.password = "12345"
# session.commit()

# #excluir
# session.delete(user)
# session.commit()
#fechando a conexão
session.close()
   

# ---------------------------------------------------------------------------------
# # Criando Conexão
# from sqlalchemy import create_engine

# conx_str = 'mysql+mysqlconnector://root@localhost:3306/task_list'
# engine = create_engine(conx_str, echo=True)


# # Criando modelo base que irá conectar
# from sqlalchemy.orm import declarative_base

# BaseModel = declarative_base()


# # Mapeando Modelos
# from sqlalchemy import Column, Integer, String, Boolean

# class User(BaseModel):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String(255), nullable=False, unique=True)
#     password = Column(String(255), nullable=False)
#     active = Column(Boolean, nullable=False, default=True)


# # Criando tabelas (Se não existirem).
# BaseModel.metadata.create_all(bind=engine)

# # Interagindo com o Banco de Dados.
# from sqlalchemy.orm import sessionmaker

# SessionLocal = sessionmaker(bind=engine)
# # Abrindo a sessão
# session = SessionLocal()

# # Operações com o banco de dados aqui.
# # Criando Usuario
# user = User(
#     username='erikrodrigues', # Não irá criar usuarios com o mesmo username
#     password='123'
# )
# session.add(user)
# session.commit()

# # Buscar todos
# users = session.query(User).all()
# print(users)

# # Buscar com condição
# user = session.query(User).filter(User.username == 'davilucciola').first()
# print(user)

# # Editar
# # user.password = 12345
# # session.commit()

# # Excluir
# # session.delete(user)
# # session.commit()

# # Fechando a sessão
# session.close()
