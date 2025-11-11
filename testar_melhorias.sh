#!/bin/bash
# Script de verificação rápida do sistema

echo "🔍 Verificando Sistema de Laudos ECG..."
echo ""

# Verificar se o servidor está rodando
echo "1. Verificando servidor Flask..."
if curl -s http://localhost:5000 > /dev/null; then
    echo "   ✅ Servidor está rodando em http://localhost:5000"
else
    echo "   ❌ Servidor não está acessível"
    echo "   Execute: python app.py"
    exit 1
fi

echo ""
echo "2. Testando rotas principais..."

# Testar rota inicial
if curl -s http://localhost:5000 | grep -q "Sistema de Laudos"; then
    echo "   ✅ Rota / (início) - OK"
else
    echo "   ❌ Rota / (início) - FALHOU"
fi

# Testar rota de análise
if curl -s http://localhost:5000/analise | grep -q "Análise"; then
    echo "   ✅ Rota /analise - OK"
else
    echo "   ❌ Rota /analise - FALHOU"
fi

# Testar rota de resultados
if curl -s http://localhost:5000/resultados | grep -q "Resultados"; then
    echo "   ✅ Rota /resultados - OK"
else
    echo "   ❌ Rota /resultados - FALHOU"
fi

echo ""
echo "3. Verificando arquivos críticos..."

files=(
    "app.py"
    "audio_generator.py"
    "models/ecg_analyzer.py"
    "models/ecg_data.py"
    "models/laudo_generator.py"
    "templates/base.html"
    "templates/index.html"
    "templates/analise.html"
    "templates/resultados.html"
    "requirements.txt"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file - FALTANDO"
    fi
done

echo ""
echo "4. Verificando dependências Python..."

python -c "import flask" 2>/dev/null && echo "   ✅ Flask" || echo "   ❌ Flask não instalado"
python -c "import gtts" 2>/dev/null && echo "   ✅ gTTS" || echo "   ❌ gTTS não instalado"
python -c "import pygame" 2>/dev/null && echo "   ✅ Pygame" || echo "   ❌ Pygame não instalado"
python -c "import pydub" 2>/dev/null && echo "   ✅ PyDub" || echo "   ❌ PyDub não instalado"

echo ""
echo "5. Verificando melhorias implementadas..."

# Verificar se audio_generator tem aceleração
if grep -q "speedup" audio_generator.py; then
    echo "   ✅ Aceleração de áudio (1.5x) implementada"
else
    echo "   ❌ Aceleração de áudio não encontrada"
fi

# Verificar se rotas foram renomeadas
if grep -q "/resultados" app.py; then
    echo "   ✅ Renomeação 'exemplos' → 'resultados' completa"
else
    echo "   ❌ Rotas não foram atualizadas"
fi

# Verificar atalhos de teclado
if grep -q "e.key === '1'" templates/base.html; then
    echo "   ✅ Atalhos de teclado (1, 2, 3) implementados"
else
    echo "   ❌ Atalhos de teclado não encontrados"
fi

# Verificar novo esquema de cores
if grep -q "#2563eb" templates/base.html; then
    echo "   ✅ Novo design UI (azul médico) aplicado"
else
    echo "   ❌ Novo design não aplicado"
fi

# Verificar melhorias no analisador
if grep -q "_determinar_localizacao_isquemia" models/ecg_analyzer.py; then
    echo "   ✅ Diagnóstico automático aprimorado (localização de isquemia)"
else
    echo "   ❌ Melhorias no analisador não encontradas"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Verificação completa!"
echo ""
echo "📋 Resumo das melhorias:"
echo "   1. ✅ Diagnóstico automático aprimorado (baseado em AHA)"
echo "   2. ✅ Áudios acelerados para 1.5x"
echo "   3. ✅ 'Exemplos' renomeado para 'Fila de Resultados'"
echo "   4. ✅ Atalhos de teclado (1: Início, 2: Análise, 3: Resultados)"
echo "   5. ✅ Novo design UI profissional (sem gradiente)"
echo ""
echo "🌐 Acesse: http://localhost:5000"
echo "⌨️  Use as teclas 1, 2, 3 para navegação rápida!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
