#!/bin/bash
# Script para aplicar refatoração do projeto

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Refatoração do Sistema de Laudos ECG ===${NC}\n"

# Diretório base
BASE_DIR="/home/br4b0/Desktop/research/medicina/new/ecg_laudo_system"

# 1. Criar backup dos arquivos originais
echo -e "${YELLOW}1. Criando backup dos arquivos originais...${NC}"
BACKUP_DIR="${BASE_DIR}/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

cp "$BASE_DIR/app.py" "$BACKUP_DIR/" 2>/dev/null
cp "$BASE_DIR/templates/base.html" "$BACKUP_DIR/" 2>/dev/null

echo -e "${GREEN}✓ Backup criado em: $BACKUP_DIR${NC}\n"

# 2. Substituir arquivos
echo -e "${YELLOW}2. Aplicando arquivos refatorados...${NC}"

# Substituir app.py
if [ -f "$BASE_DIR/app_new.py" ]; then
    mv "$BASE_DIR/app.py" "$BASE_DIR/app_old.py"
    mv "$BASE_DIR/app_new.py" "$BASE_DIR/app.py"
    echo -e "${GREEN}✓ app.py refatorado${NC}"
fi

# Substituir base.html
if [ -f "$BASE_DIR/templates/base_new.html" ]; then
    mv "$BASE_DIR/templates/base.html" "$BASE_DIR/templates/base_old.html"
    mv "$BASE_DIR/templates/base_new.html" "$BASE_DIR/templates/base.html"
    echo -e "${GREEN}✓ base.html refatorado${NC}"
fi

echo ""

# 3. Verificar estrutura
echo -e "${YELLOW}3. Verificando nova estrutura...${NC}"

dirs=("routes" "services" "data" "static/js" "static/css")
for dir in "${dirs[@]}"; do
    if [ -d "$BASE_DIR/$dir" ]; then
        echo -e "${GREEN}✓ $dir${NC}"
    else
        echo -e "${RED}✗ $dir não encontrado${NC}"
    fi
done

echo ""

# 4. Listar arquivos criados
echo -e "${YELLOW}4. Novos arquivos criados:${NC}"
echo ""
echo "Backend:"
echo "  - config.py (configurações centralizadas)"
echo "  - routes/main.py (rotas de páginas)"
echo "  - routes/api.py (rotas de API)"
echo "  - services/ecg_service.py (lógica de análise)"
echo "  - services/audio_service.py (gerenciamento de áudio)"
echo "  - data/ecg_examples.py (dados de exemplo)"
echo ""
echo "Frontend:"
echo "  - static/css/main.css (estilos)"
echo "  - static/js/audio.js (controle de áudio e mute)"
echo "  - static/js/keyboard.js (atalhos de teclado)"
echo "  - static/js/accessibility.js (sistema de acessibilidade)"
echo ""

# 5. Instruções
echo -e "${YELLOW}5. Próximos passos:${NC}"
echo ""
echo "Para testar a aplicação refatorada:"
echo "  cd $BASE_DIR"
echo "  python app.py"
echo ""
echo "Para reverter para a versão antiga (se necessário):"
echo "  mv $BASE_DIR/app.py $BASE_DIR/app_refatorado.py"
echo "  mv $BASE_DIR/app_old.py $BASE_DIR/app.py"
echo "  mv $BASE_DIR/templates/base.html $BASE_DIR/templates/base_refatorado.html"
echo "  mv $BASE_DIR/templates/base_old.html $BASE_DIR/templates/base.html"
echo ""
echo -e "${GREEN}=== Refatoração completa! ===${NC}"
