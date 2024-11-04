import sys
from typing import List, Dict, Union
from pydantic import BaseModel, Field
sys.path.append(r"C:\Users\henri\Documents\LangChain\api_ollama\metodos\consultas")
from consulta import *

# Classe para consulta de pautas
class ConsultaPautas(Consulta):
    def __init__(self, db: Chroma, dados="") -> None:
        super().__init__(db, dados)
        self.setSystem("""
        Você é responsável por extrair informações com base no pedido do usuário. A resposta deve ser formatada estritamente em JSON, sem nenhum texto adicional ou explicações.
        Utilize o seguinte contexto:

        ========= CONTEXTO =========
        Contexto principal:
        {contexto}

        {dados}

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
        self.setQueryText("Identifique as pautas propostas no texto fornecido e associe-as às respectivas entidades proponentes, se houver.")

    # Método para definir o formato do JSON
    def formatacao(self) -> type:
        class Format(BaseModel):
            pautas_independentes: List[str] = Field(
                default_factory=list, 
                description="Lista de pautas propostas que não estão associadas a nenhuma entidade"
            )
            entidades_proponentes: List[Dict[str, Union[str, List[str]]]] = Field(
                default_factory=list, 
                description="Lista de entidades proponentes com suas pautas associadas"
            )

        return Format
    


    # Exemplo de estrutura de dados esperada
    def dataExemple(self) -> str:
        formatacao = self.formatacao()
        data: BaseModel = formatacao(
            pautas_independentes=["Pauta 1", "Pauta 2", "Pauta 3"],
            entidades_proponentes=[
                {"Nome": "Entidade A", "pautas": ["Pauta A1", "Pauta A2"]},
                {"Nome": "Entidade B", "pautas": ["Pauta B1"]}
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
