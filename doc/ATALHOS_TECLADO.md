# 📋 Sistema de Atalhos de Teclado - Apenas Numérico

## ✅ Atalhos Implementados

O sistema agora usa **APENAS** os seguintes caracteres para atalhos:
- **Números**: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
- **Operadores**: /, *, -, +, .

## 🌐 Atalhos Globais (Funcionam em Todas as Páginas)

| Tecla | Função | Descrição |
|-------|--------|-----------|
| **-** (menos) | Menu de Navegação | Ativa menu principal com opções 1, 2, 3 |
| **/** (barra) | Ajuda | Lista TODOS os atalhos disponíveis (globais + contextuais) |
| ***** (vezes) | Repetir | Repete o último anúncio de áudio |
| **+** (mais) | Mute/Unmute | Liga ou desliga o áudio do sistema |

## 📍 Menu de Navegação (Após pressionar -)

Quando você pressiona **-**, o menu de navegação é ativado. Então pressione:

| Tecla | Destino |
|-------|---------|
| **1** | Página Inicial |
| **2** | Módulo ECG |
| **3** | Módulo Hemograma |
| **0** | Cancelar menu |

## 📄 Atalhos Contextuais por Página

### Página Inicial (/)

| Tecla | Ação |
|-------|------|
| **1** | Ir para Módulo ECG |
| **2** | Ir para Módulo Hemograma |

### Página Módulo ECG (/ecg)

| Tecla | Ação |
|-------|------|
| **1** | Análise de ECG por Dados |
| **2** | Análise de ECG por Imagem |
| **3** | Fila de Resultados de ECG |
| **0** | Voltar ao Início |

### Página Módulo Hemograma (/hemograma)

| Tecla | Ação |
|-------|------|
| **1** | Nova Análise de Hemograma |
| **2** | Ver Exemplos de Hemogramas |
| **0** | Voltar ao Início |

### Página de Análise de ECG (/analise)

| Tecla | Ação |
|-------|------|
| **1** | Carregar Exemplo Normal |
| **2** | Carregar Exemplo Arritmia |
| **3** | Carregar Exemplo Infarto |
| **4** | Gerar Laudo |
| **5** | Reproduzir Áudio do Laudo |
| **6** | Pausar/Retomar Áudio |
| **7** | Copiar Laudo |
| **8** | Limpar Formulário |
| **0** | Voltar ao Módulo ECG |

### Página de Análise por Imagem (/analise-imagem)

| Tecla | Ação |
|-------|------|
| **1** | Selecionar Arquivo |
| **2** | Enviar para Análise |
| **0** | Voltar ao Módulo ECG |

### Página de Resultados ECG (/resultados)

| Tecla | Ação |
|-------|------|
| **1** | Ver Resultado Normal |
| **2** | Ver Resultado Arritmia |
| **3** | Ver Resultado Bloqueio |
| **4** | Voltar à Lista |
| **5** | Copiar Laudo |
| **6** | Reproduzir Áudio |
| **7** | Pausar/Retomar Áudio |
| **0** | Voltar ao Módulo ECG |

### Página de Análise de Hemograma (/hemograma/analise)

| Tecla | Ação |
|-------|------|
| **1** | Carregar Exemplo Normal |
| **2** | Carregar Exemplo Anemia |
| **3** | Carregar Exemplo Leucocitose |
| **4** | Carregar Exemplo Plaquetopenia |
| **5** | Analisar Hemograma |
| **6** | Limpar Formulário |
| **7** | Copiar Laudo |
| **0** | Voltar ao Módulo Hemograma |

### Página de Exemplos de Hemograma (/hemograma-resultados)

| Tecla | Ação |
|-------|------|
| **1** | Analisar Exemplo Normal |
| **2** | Analisar Exemplo Anemia |
| **3** | Analisar Exemplo Leucocitose |
| **4** | Analisar Exemplo Plaquetopenia |
| **5** | Copiar Laudo |
| **6** | Fechar Resultado |
| **0** | Voltar ao Módulo Hemograma |

## 🎯 Como Usar o Sistema Apenas com Teclado

### Exemplo 1: Analisar um ECG

1. Na página inicial, pressione **1** → Vai para Módulo ECG
2. Pressione **1** → Vai para Análise por Dados
3. Pressione **1** → Carrega exemplo normal
4. Pressione **4** → Gera o laudo
5. Pressione **5** → Ouve o laudo em áudio
6. Pressione **7** → Copia o laudo

### Exemplo 2: Analisar um Hemograma

1. Na página inicial, pressione **2** → Vai para Módulo Hemograma
2. Pressione **1** → Vai para Nova Análise
3. Pressione **2** → Carrega exemplo de anemia
4. Pressione **5** → Analisa o hemograma
5. O áudio é tocado automaticamente

### Exemplo 3: Navegar entre Módulos

1. Em qualquer página, pressione **-** → Ativa menu de navegação
2. Pressione **2** → Vai para Módulo ECG
3. Pressione **-** novamente → Menu de navegação
4. Pressione **3** → Vai para Módulo Hemograma

### Exemplo 4: Usar Ajuda

1. Em qualquer página, pressione **/** → Lista TODOS os atalhos
2. O sistema lê em áudio todos os atalhos globais e contextuais

### Exemplo 5: Repetir Último Anúncio

1. Se você perdeu o que foi dito, pressione ***** 
2. O último anúncio será repetido

### Exemplo 6: Mutar/Desmutar

1. Pressione **+** → Muta o áudio
2. Pressione **+** novamente → Desmuta

## 🔊 Sistema de Anúncios

Cada ação gera um anúncio de áudio que:

1. **Informa o que está acontecendo** (ex: "Carregando exemplo normal")
2. **É salvo** para poder ser repetido com *****
3. **Pode ser mutado** com **+**
4. **Não interfere** em campos de texto (pode digitar normalmente)

## 💡 Dicas

- **Pressione / para ajuda** em qualquer momento
- **Use - para navegação rápida** entre módulos
- **Use * para repetir** se não ouviu bem
- **Use + para silenciar** se estiver em ambiente público
- **Números 0-9** fazem ações específicas de cada página
- **Tecla 0** geralmente volta uma página atrás

## 🚀 Compatibilidade

✅ **Teclado principal**: Funciona com os números e operadores normais
✅ **Numpad**: Funciona com o teclado numérico lateral
✅ **Screen readers**: Compatível com NVDA, JAWS, etc.
✅ **Navegadores**: Chrome, Firefox, Edge, Safari

## 📝 Observações Importantes

1. **Atalhos NÃO funcionam** quando você está digitando em um campo de texto
2. **Estado de mute** é salvo entre páginas (persiste)
3. **Último anúncio** só repete SE houve um anúncio antes
4. **Ajuda (/)** sempre mostra os atalhos da página atual
5. **Menu (-)** permite navegar globalmente

## 🔧 Mudanças em Relação ao Sistema Anterior

### ❌ Removido:
- Letra **H** para ajuda → Agora é **/**
- Letra **M** para mute → Agora é **+**
- Outras letras do alfabeto

### ✅ Adicionado:
- ***** para repetir último anúncio
- **/** para ajuda completa
- **0** para voltar/cancelar
- Sistema unificado apenas com números e operadores

### ✨ Melhorado:
- Anúncios mais detalhados
- Feedback em todas as ações
- Navegação totalmente por números
- Compatibilidade total com numpad
