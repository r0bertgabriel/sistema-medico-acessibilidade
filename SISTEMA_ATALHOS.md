# 🎹 Sistema de Navegação Contextual - Guia Rápido

## ✅ Mudanças Implementadas

### 1. Aviso Removido
❌ Removido: "⚠️ Importante: Os laudos são ferramentas de apoio diagnóstico..."

### 2. Novo Sistema de Atalhos Inteligente

#### Como Funciona:
- **Cada página tem seus próprios atalhos numéricos**
- **Tecla `-` (hífen)** ativa o menu principal de navegação
- **Tecla `H`** mostra ajuda com todos os atalhos disponíveis
- **Feedback auditivo** em todas as ações

---

## 🎮 Atalhos por Página

### 📍 Página Inicial (`http://localhost:5000/`)

| Tecla | Ação |
|-------|------|
| `1` | Ir para Nova Análise |
| `2` | Ir para Fila de Resultados |
| `-` | Menu principal |
| `H` | Ajuda (lista atalhos) |

**Ao entrar**: Ouve "Atalhos disponíveis: 1 para Ir para Nova Análise. 2 para Ir para Fila de Resultados. Hífen para menu principal."

---

### 📊 Página de Análise (`http://localhost:5000/analise`)

| Tecla | Ação |
|-------|------|
| `Enter` | **Gerar laudo** (atalho principal!) |
| `1` | Focar no primeiro campo (Frequência Cardíaca) |
| `C` | Copiar laudo para área de transferência |
| `R` | Reproduzir áudio do laudo |
| `P` | Pausar/Continuar áudio |
| `-` | Menu principal |
| `H` | Ajuda |

**Fluxo de uso**:
1. Preencha os campos usando Tab
2. Pressione `Enter` para gerar laudo (não precisa clicar no botão!)
3. Pressione `R` para ouvir novamente
4. Pressione `C` para copiar

**Ao entrar**: Ouve "Atalhos disponíveis: Enter para Gerar laudo. 1 para Focar no primeiro campo. C para Copiar laudo. R para Reproduzir áudio. P para Pausar/Continuar. Hífen para menu principal."

---

### 📋 Página de Resultados (`http://localhost:5000/resultados`)

| Tecla | Ação |
|-------|------|
| `1` | Processar resultado **Normal** |
| `2` | Processar resultado **Arritmia Sinusal** |
| `3` | Processar resultado **Bloqueio de Ramo** |
| `V` | Voltar à lista de resultados |
| `C` | Copiar laudo atual |
| `R` | Reproduzir áudio |
| `P` | Pausar/Continuar áudio |
| `-` | Menu principal |
| `H` | Ajuda |

**Fluxo de uso**:
1. Pressione `1`, `2` ou `3` para processar um resultado (não precisa clicar!)
2. Ouça o laudo automaticamente
3. Pressione `V` para voltar
4. Pressione `C` para copiar

**Ao entrar**: Ouve "Atalhos disponíveis: 1 para Processar resultado Normal. 2 para Processar resultado Arritmia Sinusal. 3 para Processar resultado Bloqueio de Ramo. V para Voltar. C para Copiar. R para Reproduzir. P para Pausar. Hífen para menu principal."

---

## 🎯 Menu Principal (Tecla `-`)

### Como Usar:
1. Pressione `-` (hífen) em **qualquer página**
2. Ouve: "Menu principal. 1 para Início. 2 para Análise ECG. 3 para Fila de Resultados."
3. Pressione `1`, `2` ou `3` para navegar
4. Ou pressione `Esc` para cancelar

### Exemplo Prático:
```
[Você está em /resultados]
↓ Pressiona -
"Menu principal. 1 para Início. 2 para Análise ECG. 3 para Fila de Resultados."
↓ Pressiona 2
"Indo para Análise ECG"
[Navega para /analise]
```

---

## 🔄 Diferenças do Sistema Antigo

### ❌ Antes (Sistema Global)
- Tecla `1`, `2`, `3` sempre navegavam para Início/Análise/Resultados
- Mesmo dentro de campos de texto (bug)
- Sem feedback auditivo ao pressionar
- Sem atalhos específicos por página
- Sem atalho para gerar laudo (tinha que clicar)

### ✅ Agora (Sistema Contextual)
- Cada página tem atalhos **diferentes e relevantes**
- Tecla `-` para navegação global (não conflita)
- Feedback auditivo em **todas** as ações
- `Enter` gera laudo em /analise
- `1`, `2`, `3` processam resultados em /resultados
- `H` mostra ajuda contextual
- Ignora teclas quando está digitando em campos

---

## 🎤 Feedback Auditivo

### O que você ouve:

#### Ao entrar na página:
```
"Atalhos disponíveis: [lista dos atalhos da página]. Hífen para menu principal."
```

#### Ao pressionar um atalho:
```
"Gerar laudo" (antes de executar)
```

#### Ao pressionar `-`:
```
"Menu principal. 1 para Início. 2 para Análise ECG. 3 para Fila de Resultados."
```

#### Ao navegar:
```
"Indo para Análise ECG"
```

#### Ao pressionar `H`:
```
"Atalhos disponíveis: [lista completa]"
```

---

## 📋 Console do Navegador

Abra o Console (F12) para ver logs detalhados:

```
🎹 Atalhos disponíveis nesta página:
  Enter - Gerar laudo
  1 - Focar no primeiro campo
  c - Copiar laudo
  r - Reproduzir áudio
  p - Pausar/Continuar áudio
  - (hífen) - Voltar ao menu principal

⚡ Atalho acionado: Enter - Gerar laudo
🔊 Anunciando: Gerar laudo

📋 Modo Menu ativado - Escolha: 1=Início, 2=Análise, 3=Resultados
➡️ Navegando para Análise ECG
```

---

## 🧪 Teste Agora!

### 1. Página Inicial
```bash
# Acesse
http://localhost:5000/

# Pressione
1  # Vai para Análise
```

### 2. Página de Análise
```bash
# Acesse
http://localhost:5000/analise

# Preencha os campos (Tab entre eles)
# Pressione
Enter  # Gera laudo (sem clicar no botão!)
R      # Reproduz áudio novamente
C      # Copia laudo
-      # Abre menu principal
```

### 3. Página de Resultados
```bash
# Acesse
http://localhost:5000/resultados

# Pressione
1  # Processa resultado Normal (sem clicar!)
V  # Volta para a lista
2  # Processa Arritmia Sinusal
-  # Menu principal
```

---

## 🎓 Dicas de Uso

### Para Usuários Cegos:
1. **Sempre ouça** o anúncio ao entrar na página
2. Pressione **`H`** se esquecer os atalhos
3. Use **`-`** quando quiser navegar entre páginas
4. Use **Tab** para navegar entre campos (com feedback auditivo)
5. Use **`Enter`** em /analise em vez de procurar o botão

### Para Desenvolvedores:
1. Console mostra **todos** os eventos de atalhos
2. Logs com emoji facilitam identificação
3. `registrarAtalhos({...})` em cada página
4. `anunciar(texto)` para feedback customizado

---

## 🐛 Troubleshooting

### Atalho não funciona?
- ✅ Verifique se não está digitando em um campo (INPUT/TEXTAREA/SELECT)
- ✅ Abra o Console (F12) e veja se há erros
- ✅ Recarregue a página com Ctrl+Shift+R

### Não ouve feedback auditivo?
- ✅ Volume do sistema está ligado?
- ✅ Console mostra "🔊 Anunciando:"?
- ✅ Aguarde 1 segundo após carregar a página

### Menu principal não abre com `-`?
- ✅ Use o hífen da linha superior (não do teclado numérico)
- ✅ Solte a tecla Shift
- ✅ Verifique no Console se aparece "📋 Modo Menu ativado"

---

## ✨ Resumo

**Sistema Antigo**: 3 atalhos globais (1, 2, 3)  
**Sistema Novo**: 7-8 atalhos por página + menu global (-)

**Benefícios**:
- ✅ Mais produtividade (Enter gera laudo!)
- ✅ Menos cliques de mouse
- ✅ Feedback constante
- ✅ Navegação não-destrutiva (- para menu)
- ✅ Ajuda contextual (H)
- ✅ Intuitivo e memorável

**Próximos Testes**:
1. Teste com usuários reais
2. Ajuste velocidade/volume do áudio se necessário
3. Adicione mais atalhos conforme feedback
