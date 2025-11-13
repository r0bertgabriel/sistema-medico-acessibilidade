#!/bin/bash
# Script de instalação do Sistema de Laudos ECG com Análise por Imagem

echo "=================================================="
echo "  Sistema de Laudos ECG - Instalação"
echo "=================================================="
echo ""

# Verificar Python
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION encontrado"
echo ""

# Criar ambiente virtual
echo "🔧 Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi
echo ""

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "⬆️  Atualizando pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✅ pip atualizado"
echo ""

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt
echo "✅ Dependências instaladas"
echo ""

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p static/audio
mkdir -p static/uploads
mkdir -p data
touch static/audio/.gitkeep
touch static/uploads/.gitkeep
echo "✅ Diretórios criados"
echo ""

# Configurar .env
echo "🔐 Configurando variáveis de ambiente..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Arquivo .env criado a partir de .env.example"
    echo ""
    echo "⚠️  IMPORTANTE: Configure sua OPENAI_API_KEY no arquivo .env"
    echo "   Para análise por imagem, você precisa de uma chave de API da OpenAI"
    echo "   Obtenha em: https://platform.openai.com/api-keys"
    echo ""
else
    echo "✅ Arquivo .env já existe"
fi
echo ""

# Verificar se OPENAI_API_KEY está configurada
if [ -f ".env" ]; then
    source .env
    if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "sk-proj-your-api-key-here" ]; then
        echo "⚠️  ATENÇÃO: OPENAI_API_KEY não configurada ou usando valor padrão"
        echo "   A análise por imagem não funcionará sem uma chave válida"
        echo ""
    else
        echo "✅ OPENAI_API_KEY configurada"
        echo ""
    fi
fi

echo "=================================================="
echo "  ✅ Instalação concluída!"
echo "=================================================="
echo ""
echo "📚 Próximos passos:"
echo ""
echo "1. Configure sua chave OpenAI (para análise por imagem):"
echo "   - Edite o arquivo .env"
echo "   - Adicione: OPENAI_API_KEY=sua-chave-aqui"
echo ""
echo "2. Inicie o servidor:"
echo "   ./run.sh"
echo "   (ou: python app.py)"
echo ""
echo "3. Acesse no navegador:"
echo "   http://localhost:5000"
echo ""
echo "📖 Documentação da análise por imagem:"
echo "   cat ANALISE_POR_IMAGEM.md"
echo ""
echo "🧪 Testar análise de imagem:"
echo "   python test_vision.py caminho/para/imagem.jpg"
echo ""
