# criar classe base para consultas
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_chroma import Chroma
import os
import sys
# criar path
sys.path.append(r"C:\Users\henri\Documents\LangChain\api_ollama\scripts")
from parseString import *
from tratar_dados import *



class Consulta():
    def __init__(self, db: Chroma, dados = "") -> None:
        self.sistema = ""
        self.db = db
        self.dados = dados
        self.human = ""
        self.query_text = ""

    # setar texto para sistema
    def setSystem(self, sistema):
        self.sistema = sistema
    
    # setar texto para sistema
    def setHuman(self, human):
        self.human = human

    def setQueryText(self, query):
        self.query_text = query

    # criar formatacao
    # implementar na classe filha
    def formatacao(self)->BaseModel:
        pass 
    # exemplo do tipo de dado que desejo receber
    def dataExemple(self)->dict:
        pass
    
    # formatar entrada de dados
    def dataFormat(self, data: dict):
        if data is None:
            return ""
        string = f"Dados fornecidos para análise:\n{getDictString(data)}" 
        return string
    
    def respostaFormat(self, resposta: dict):
        if resposta is None:
            return ""
        string = f"Respostas processadas até agora:\n{getDictString(resposta)}"
        return string
    # realizar query dos dados
    def get_context(self):
        chunk_qunt = int(len(self.db.get()['ids'])/4)
        result = self.db.similarity_search_with_score(self.query_text, k=chunk_qunt)
        context_text = "\n\n".join([doc.page_content for doc, score in result])
        return context_text


    # realizar consulta para llm
    def consultarLLM(self, LLM: OllamaLLM, dados = None, respotas = None):
        dados = self.dataFormat(dados)
        respotas = self.respostaFormat(respotas)
        contexto = self.get_context()
        parser = JsonOutputParser(pydantic_object=self.formatacao())

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.sistema),
                ("human", self.human)
            ]
        )
        chain = prompt | LLM | parser
        response = chain.invoke(
            {
                "contexto":contexto,
                "format":parser.get_format_instructions(),
                "pergunta":self.query_text,
                "dados":dados,
                "respostas": respotas,
                "exemplo":self.dataExemple()
            }
        )

        return response
    
    # realizar processo encadeado
    def consultasEncadeadas(self):
        pass
    

