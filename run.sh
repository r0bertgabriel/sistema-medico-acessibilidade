#!/bin/bash
# Script para executar o Sistema de Laudos ECG

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Carregar variáveis de ambiente
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

echo "=================================================="
echo "  Sistema de Laudos ECG - Iniciando"
echo "=================================================="
echo ""
echo "🚀 Servidor iniciando em http://localhost:5000"
echo ""
echo "📌 Funcionalidades disponíveis:"
echo "   • Análise de ECG por dados (JSON)"
echo "   • Análise de ECG por imagem (GPT-4o Vision)"
echo "   • Geração automática de laudos"
echo "   • Conversão para áudio acessível"
echo ""
echo "⌨️  Pressione Ctrl+C para parar"
echo ""
echo "=================================================="
echo ""

# Iniciar aplicação
python app.py
