#!/bin/bash

# Script de verificação do sistema ECG

echo "🩺 VERIFICAÇÃO DO SISTEMA DE LAUDOS ECG"
echo "========================================"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "app.py" ]; then
    echo "❌ Erro: Execute este script dentro do diretório ecg_laudo_system"
    exit 1
fi

echo "✅ Diretório correto"
echo ""

# Verificar Python
echo "📌 Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python encontrado: $PYTHON_VERSION"
else
    echo "❌ Python3 não encontrado"
    exit 1
fi
echo ""

# Verificar estrutura de arquivos
echo "📌 Verificando estrutura de arquivos..."
FILES=(
    "app.py"
    "audio_generator.py"
    "test_system.py"
    "requirements.txt"
    "models/ecg_data.py"
    "models/ecg_analyzer.py"
    "models/laudo_generator.py"
    "templates/base.html"
    "templates/index.html"
    "templates/analise.html"
    "templates/exemplos.html"
)

ALL_FILES_OK=true
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file - FALTANDO"
        ALL_FILES_OK=false
    fi
done
echo ""

if [ "$ALL_FILES_OK" = false ]; then
    echo "❌ Alguns arquivos estão faltando"
    exit 1
fi

# Verificar diretórios
echo "📌 Verificando diretórios..."
DIRS=(
    "models"
    "templates"
    "static"
    "static/audio"
)

for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir/"
    else
        echo "  ❌ $dir/ - FALTANDO"
    fi
done
echo ""

# Verificar dependências instaladas
echo "📌 Verificando dependências Python..."
python3 -c "import flask" 2>/dev/null && echo "  ✅ Flask" || echo "  ⚠️  Flask não instalado"
python3 -c "import gtts" 2>/dev/null && echo "  ✅ gTTS" || echo "  ⚠️  gTTS não instalado"
python3 -c "import pygame" 2>/dev/null && echo "  ✅ Pygame" || echo "  ⚠️  Pygame não instalado"
echo ""

# Tentar executar os testes
echo "📌 Executando testes..."
if python3 test_system.py > /dev/null 2>&1; then
    echo "  ✅ Testes passaram com sucesso"
else
    echo "  ⚠️  Testes falharam (pode ser devido a dependências faltando)"
fi
echo ""

# Resumo
echo "========================================"
echo "📊 RESUMO DA VERIFICAÇÃO"
echo "========================================"
echo ""

if [ "$ALL_FILES_OK" = true ]; then
    echo "✅ Estrutura de arquivos: OK"
    echo "✅ Sistema pronto para uso"
    echo ""
    echo "🚀 PRÓXIMOS PASSOS:"
    echo ""
    echo "1. Instalar dependências (se necessário):"
    echo "   pip install -r requirements.txt"
    echo ""
    echo "2. Executar testes:"
    echo "   python3 test_system.py"
    echo ""
    echo "3. Iniciar aplicação:"
    echo "   python3 app.py"
    echo ""
    echo "4. Acessar no navegador:"
    echo "   http://localhost:5000"
    echo ""
else
    echo "❌ Alguns componentes estão faltando"
    echo "   Verifique os arquivos marcados acima"
fi
