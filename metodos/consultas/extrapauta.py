import sys
from langchain_chroma import Chroma
from pydantic import BaseModel, Field
from typing import List, Dict, Union
sys.path.append(r"C:\Users\henri\Documents\LangChain\api_ollama\metodos\consultas")
from consulta import *

# Classe para consulta das extrapautas
class ConsultaExtrapauta(Consulta):
    def __init__(self, db: Chroma, dados="") -> None:
        super().__init__(db, dados)
        self.setSystem("""
        Você é responsável por extrair as informações necessárias com base no pedido do usuário. As respostas devem ser formatadas estritamente em JSON, sem nenhum texto adicional ou explicações.
        Utilize o seguinte contexto:

        ========= CONTEXTO =========
        Contexto principal:
        {contexto}

        Dados fornecidos para análise:
        {dados}

        Respostas processadas até agora:
        {respostas}
        ===== FIM DO CONTEXTO ======

        Certifique-se de que sua resposta siga o seguinte formato JSON:
        {format}
        A resposta deve ser um JSON completamente válido.
        """)

        self.setHuman("""
        Por favor, extraia as informações conforme solicitado abaixo:

        {pergunta}

        A resposta deve ser formatada em JSON. Use o exemplo abaixo **somente** como referência de formatação, os dados reais virão da consulta:

        Exemplo de formato JSON:
        {exemplo}

        Garanta que sua resposta siga rigorosamente essa estrutura.
        """)

        # Texto da consulta principal
        self.setQueryText("Identifique as **pautas extras** propostas no texto fornecido e associe-as às respectivas entidades proponentes, se houver.")

    # Método para definir o formato do JSON
    def formatacao(self) -> BaseModel:
        class Format(BaseModel):
            pautas_independentes: List[str] = Field(
                default_factory=list, 
                description="Pautas extras propostas sem associação a nenhuma entidade"
            )
            entidades_proponentes: List[Dict[str, Union[str, List[str]]]] = Field(
                default_factory=list, 
                description="Lista de entidades proponentes com suas pautas extras associadas"
            )

        return Format
    
    # Exemplo de estrutura de dados esperada
    def dataExemple(self) -> str:
        formatacao = self.formatacao()
        data: BaseModel = formatacao(
            pautas_independentes=["Pauta Extra 1", "Pauta Extra 2", "Pauta Extra 3"],
            entidades_proponentes=[
                {"Nome": "Entidade A", "pautas": ["Pauta Extra A1", "Pauta Extra A2"]},
                {"Nome": "Entidade B", "pautas": ["Pauta Extra B1"]}
            ]
        )
        return getDictString(data.model_dump())
    
    # Método para lidar com consultas encadeadas
    def consultasEncadeadas(self, LLM: OllamaLLM):
        primeira_resposta = self.consultarLLM(LLM)
        format_response = f"\nResposta anterior:\n{getDictString(primeira_resposta)}"
        
        if isinstance(self.dados, dict):
            dados_user = f"\nDados fornecidos pelo usuário:\n{getDictString(self.dados)}"
            final_response = self.consultarLLM(LLM, dados_user, format_response)
        else:
            final_response = self.consultarLLM(LLM, respostas=format_response)
        
        return final_response
