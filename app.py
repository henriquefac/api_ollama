from flask import Flask, request, jsonify, session
import chardet
import base64
import os
from langchain_ollama import OllamaLLM
from scripts.parseString import *
from metodos.rag import RagGen
from metodos.consultas.pautas import ConsultaPautas
from metodos.consultas.extrapauta import ConsultaExtrapauta

app = Flask(__name__)

app.secret_key = "shhh, segredo fi"


# passar para formato json
def jfy(dado):
    return {"dado": dado}

# endpoint para receber dados de upload
@app.route("/upload", methods=['POST'])
def upload():
    dados: dict = request.get_json()
    
    # A partir do arquivo, gerar sugestões para cada campo
    payload = jfy(dados)

    # Decodificando e armazenando na sessão
    text64encode = dados.get("dado")  # Supondo que "dado" seja a chave correta
    decode_data = base64.b64decode(text64encode)
    texto_decodificado = decode_data.decode('utf-8')
    session['dados'] = texto_decodificado
    

    # Realizar a consulta
    return request_content()  # Chame a função de consulta diretamente

# endpoint para realizar consultas
@app.route("/consulta", methods=["GET"])  # Mantendo a rota
def request_content():
    # LLM para consulta
    url = os.getenv("BASE_ACCES")
    #url = "http://10.10.0.98:11434"
    LLM = OllamaLLM(
        base_url=url,
        model="llama3.2",
        temperature=0
    )
    
    # consulta final
    resposta_fim = {}

    # db para acessar as informações armazenadas na sessão
    try:
        
        db = RagGen(session['dados']).get_vector_store()
        print("Fazer consulta")
        pauta = ConsultaPautas(db).consultarLLM(LLM)
        
        resposta_fim["pautas"] = pauta
        print(resposta_fim)
        extrapauta = ConsultaExtrapauta(db).consultarLLM(LLM)
        resposta_fim["pautas extras"] = extrapauta
        print(getDictString(resposta_fim))
        print(type(extrapauta))
        # Retornar o resultado da consulta em formato JSON
        resposta = {
            "status": "sucesso",
            "repostas": resposta_fim
        }
        return jsonify(resposta), 200
    except Exception as e:
        print(f"Erro ao realizar a consulta: {e}")  # Log do erro
        # Se não houver dados na sessão
        resposta = {
            "status": "erro",
            "mensagem": "Nenhuma informação disponível na sessão."
        }
        return jsonify(resposta), 400

# endpoint para receber dados de upload
@app.route("/tetse_dict", methods=['POST'])
def dict_teste():
    dict_ = request.get_json()["dado"]
    print(getDictString(dict_))
    resposta = {
            "status": "sucesso",
            "mensagem": "Dados recebidos e processados!"       
    }
    return jsonify(resposta), 200



if __name__ == "__main__":
    app.run(debug=True)