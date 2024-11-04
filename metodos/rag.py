from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os, sys, shutil

# Caminho customizado para scripts
my_path = os.path.join(os.path.abspath(__file__).rsplit("\\", 2)[0], "scripts")
sys.path.append(my_path)

from tratar_dados import *

# Classe responsável por lidar com os dados e gerar o reg
class RagGen():
    def __init__(self, dados: str) -> None:
        # Dados filtrados
        self.dados = filtrar(dados)
        self.dir = r"C:\Users\henri\Documents\LangChain\api_ollama\db"

    # Gerar nome para o diretório do Chroma
    def getName(self):
        name = self.dados.split("\n")
        # Combina as primeiras letras das três primeiras linhas
        name = name[0][0] + name[1][0] + name[2][0]
        return name

    # Dividir dados em chunks
    def getChunks(self):
        document = self.dados
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=50,
            length_function=len
        )
        chunks = text_splitter.split_text(document)
        print(len(chunks))
        return chunks
    
    # Criar embedding
    def get_embedding(self, chunks, dbname):
        # Certifique-se de que a variável de ambiente BASE_ACCES esteja definida corretamente
        #base_url = os.getenv("BASE_ACCES")
        base_url = "http://10.10.0.98:11434"
        if not base_url:
            raise ValueError("Variável de ambiente BASE_ACCES não definida.")
        
        ollama_embed = OllamaEmbeddings(
            base_url=base_url,
            model="nomic-embed-text"
        )
        
        # Persistir o banco de dados no diretório especificado
        db = Chroma.from_texts(
            texts=chunks, 
            embedding=ollama_embed, 
            persist_directory=os.path.join(self.dir, dbname)
        )
        return db
    
    # Carregar ou criar o banco de dados Chroma
    def get_vector_store(self):
        name = self.getName()
        db_dir = os.path.join(self.dir, name)
        
        # Certifique-se de que o diretório existe
        os.makedirs(db_dir, exist_ok=True)
        
        # Se o diretório não estiver vazio, carregar o banco de dados existente
        if os.path.isdir(db_dir) and os.listdir(db_dir):
            print("existe")
            db = Chroma(
                persist_directory=db_dir, 
                embedding_function=OllamaEmbeddings(
                    base_url=os.getenv("BASE_ACCES"), 
                    model="nomic-embed-text"
                )
            )
            return db
        else:
            # Caso o diretório esteja vazio, criar um novo banco de dados
            chunks = self.getChunks()
            db = self.get_embedding(chunks, name)
            return db
    


    # quando a consulta acabar, apagar diretório
    # função para apagar diretório
    def delete_chroma_db(self):
        name = self.getName()
        db_dir = os.path.join(self.dir, name)
        if os.path.exists(db_dir):
        # Remove o diretório e todo o conteúdo
            shutil.rmtree(db_dir)