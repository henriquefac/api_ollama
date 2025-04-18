#!/bin/bash

echo "Iniciando projet"

# Verifica se o ambiente já existe

if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual"
    python3 -m venv .venv

    # define as variáveis de ambiente para o ambiente vritual
    echo "export PYTHONPATH=$(PWD)" >> .venv/bin/active
    
    source .venv/bin/activate

    python -m pip install --upgrade pip

    # verifica se requirements existe
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "Aviso: requirements.txt não encontrado. Nenhum pacote foi instalado"
    fi

    deactivate
fi

source .venv/bin/activate
