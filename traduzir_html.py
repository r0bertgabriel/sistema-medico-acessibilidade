#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para traduzir termos em português para espanhol nos arquivos HTML
"""

import os
import re

# Dicionário de traduções português -> espanhol
TRADUCOES = {
    # Títulos e cabeçalhos
    "Análise de ECG": "Análisis de ECG",
    "Análise de Eletrocardiograma": "Análisis de Electrocardiograma",
    "Análise por Imagem - Sistema de Laudos ECG": "Análisis por Imagen - Sistema de Informes ECG",
    "Análise de ECG por Imagem": "Análisis de ECG por Imagen",
    "Análise da Inteligência Artificial": "Análisis de la Inteligencia Artificial",
    
    # Formulários e campos
    "Frequência Cardíaca": "Frecuencia Cardíaca",
    "Frequência cardíaca em batimentos por minuto": "Frecuencia cardíaca en latidos por minuto",
    "Intervalo PR": "Intervalo PR",
    "Intervalo QT": "Intervalo QT",
    "Intervalo QRS": "Intervalo QRS",
    "Intervalos (em segundos)": "Intervalos (en segundos)",
    "Intervalos": "Intervalos",
    "em segundos": "en segundos",
    
    # Botões e ações
    "Enviar": "Enviar",
    "Limpar": "Limpiar",
    "Carregar Exemplo": "Cargar Ejemplo",
    "Carregar": "Cargar",
    "Digite": "Ingrese",
    "Digite seu nome": "Ingrese su nombre",
    "Digite sua idade": "Ingrese su edad",
    "Nova Análise": "Nuevo Análisis",
    "Voltar ao Início": "Volver al Inicio",
    "Voltar": "Volver",
    "Ver Resultados": "Ver Resultados",
    
    # Navegação
    "Fila de Resultados": "Cola de Resultados",
    "Ir para fila de resultados": "Ir a cola de resultados",
    "Ir para análise por dados": "Ir a análisis por datos",
    "Ir para análise por imagem": "Ir a análisis por imagen",
    
    # Unidades
    " bpm": " lpm",
    "(bpm)": "(lpm)",
    "batimentos por minuto": "latidos por minuto",
    
    # Termos médicos
    "Série Vermelha": "Serie Roja",
    "Série Branca": "Serie Blanca",
    "Hemácias": "Eritrocitos",
    "Leucócitos": "Leucocitos",
    
    # Termos gerais
    "Focar no primeiro campo": "Enfocar en el primer campo",
    "Resultado da análise": "Resultado del análisis",
    "Formulário de análise": "Formulario de análisis",
    "faixa normal": "rango normal"
}

def traduzir_arquivo(caminho_arquivo):
    """Traduz um arquivo HTML"""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        conteudo_original = conteudo
        
        # Aplicar todas as traduções
        for pt, es in TRADUCOES.items():
            conteudo = conteudo.replace(pt, es)
        
        # Verificar se houve mudanças
        if conteudo != conteudo_original:
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            print(f"✅ Traduzido: {caminho_arquivo}")
            return True
        else:
            print(f"⏭️  Sem alterações: {caminho_arquivo}")
            return False
            
    except Exception as e:
        print(f"❌ Erro em {caminho_arquivo}: {e}")
        return False

def main():
    """Função principal"""
    base_dir = "/home/br4b0/Desktop/research/medicina/new/ecg_laudo_system/templates"
    
    # Arquivos para traduzir
    arquivos = [
        "analise.html",
        "analise_imagem.html",
        "resultados.html",
        "hemograma.html",
        "hemograma_resultados.html",
        "teste_acessibilidade.html",
    ]
    
    print("=" * 60)
    print("TRADUÇÃO DE ARQUIVOS HTML - PORTUGUÊS PARA ESPANHOL")
    print("=" * 60)
    
    traduzidos = 0
    for arquivo in arquivos:
        caminho = os.path.join(base_dir, arquivo)
        if os.path.exists(caminho):
            if traduzir_arquivo(caminho):
                traduzidos += 1
        else:
            print(f"⚠️  Arquivo não encontrado: {caminho}")
    
    print("=" * 60)
    print(f"✅ Total de arquivos traduzidos: {traduzidos}/{len(arquivos)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
