# 🎹 Hierarquia de Atalhos de Teclado - Documentação

## 📊 Visão Geral da Hierarquia

```
┌─────────────────────────────────────────────────────────────┐
│                    TECLA PRESSIONADA                        │
│                    (após tradução numpad)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │  Tecla permitida?    │
            │  (0-9, /, *, -, +)   │
            └──────┬───────────────┘
                   │ SIM
                   ▼
            ┌──────────────────────┐
            │  Em campo de texto?  │
            └──────┬───────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
       SIM                   NÃO
        │                     │
        ▼                     ▼
  ┌────────────┐      ┌─────────────────┐
  │ Utilitário?│      │  HIERARQUIA     │
  │ (-, /, *, +)│     │  COMPLETA       │
  └──┬─────────┘      └────────┬────────┘
     │                         │
    SIM                        ▼
     │                  ╔══════════════════╗
     │                  ║  1️⃣ MODO MENU    ║
     │                  ║     ATIVO?       ║
     │                  ╚═══════┬══════════╝
     │                          │
     │                   ┌──────┴──────┐
     │                  SIM           NÃO
     │                   │              │
     │                   ▼              ▼
     │            ┌─────────────┐  ╔══════════════╗
     │            │ NAVEGAÇÃO   │  ║ 2️⃣ UTILITÁRIO ║
     │            │ 1,2,3,0     │  ║   -, /, *, + ║
     │            └─────────────┘  ╚═══════┬══════╝
     │                                     │
     │                                    NÃO
     │                                     │
     └──────────────►(EXECUTA)◄───────────┤
                                           ▼
                                    ╔══════════════╗
                                    ║ 3️⃣ CONTEXTUAL ║
                                    ║   0-9 página ║
                                    ╚══════════════╝
```

---

## 🎯 Camadas do Sistema (Ordem de Prioridade)

### **1️⃣ MODO MENU** (Prioridade MÁXIMA)
**Ativação:** Pressione `-` (menu de navegação)  
**Estado:** `Estado.modoMenuAtivo = true`

Quando ativo, as teclas **0-9** mudam de função:

| Tecla | Função Normal | Função no Menu |
|-------|---------------|----------------|
| `1`   | Atalho contextual | 🏠 Página Inicial |
| `2`   | Atalho contextual | ❤️ Módulo ECG |
| `3`   | Atalho contextual | 🩸 Módulo Hemograma |
| `0`   | Atalho contextual | ❌ Cancelar Menu |

**Comportamento:**
- Após executar opção 1, 2 ou 3 → **desativa automaticamente**
- Opção `0` → desativa explicitamente sem navegar
- Qualquer outra tecla → anuncia "opção não existe"

---

### **2️⃣ ATALHOS UTILITÁRIOS** (Sempre disponíveis)

| Tecla | Nome | Função | Disponível em Texto? |
|-------|------|--------|---------------------|
| `-`   | Menu | Ativa modo menu de navegação | ✅ Não |
| `/`   | Ajuda | Lista todos os atalhos disponíveis | ✅ Não |
| `*`   | Repetir | Repete último anúncio de áudio | ✅ Não |
| `+`   | Mute | Alterna mutar/desmutar áudio | ✅ Não |

**Características:**
- Funcionam em **qualquer página**
- **NÃO funcionam** dentro de INPUT/TEXTAREA (para não atrapalhar digitação)
- Não são afetados pelo modo menu

---

### **3️⃣ ATALHOS CONTEXTUAIS** (Dependem da página)

Usam teclas **0-9** com ações específicas de cada página.

#### **Exemplo: Página Inicial (`/`)**
```javascript
registrarAtalhos({
    '1': { nome: 'Módulo ECG', acao: () => location.href = '/ecg' },
    '2': { nome: 'Módulo Hemograma', acao: () => location.href = '/hemograma' }
});
```

#### **Exemplo: Hub ECG (`/ecg`)**
```javascript
registrarAtalhos({
    '1': { nome: 'Análise por Dados', acao: () => location.href = '/analise' },
    '2': { nome: 'Análise por Imagem', acao: () => location.href = '/analise-imagem' },
    '3': { nome: 'Ver Exemplos', acao: () => location.href = '/resultados' },
    '0': { nome: 'Voltar', acao: () => history.back() }
});
```

**Características:**
- Cada página define seus próprios atalhos
- Limpeza automática ao trocar de página
- Anunciados automaticamente ao pressionar tecla

---

## 🔄 Fluxo de Processamento

### **Passo a Passo do Processamento:**

```javascript
1. Tecla pressionada (ex: "1")
   ↓
2. Traduzir numpad (Numpad1 → "1")
   ↓
3. Validar permitida? (0-9, /, *, -, +, .)
   ↓ SIM
4. Está em campo de texto?
   ├─ SIM → só processa utilitários
   └─ NÃO → continua
   ↓
5. Modo menu ativo?
   ├─ SIM → executa MENU_NAVEGACAO["1"] → Página Inicial
   └─ NÃO → continua
   ↓
6. É utilitário? (-, /, *, +)
   ├─ SIM → executa UTILITARIOS["-"] → Ativa Menu
   └─ NÃO → continua
   ↓
7. Atalho contextual definido?
   ├─ SIM → executa Estado.atalhosContextuais["1"]
   └─ NÃO → ignora silenciosamente
```

---

## 🎮 Exemplos de Uso

### **Cenário 1: Navegação rápida entre módulos**
```
Usuário na página de ECG quer ir para Hemograma:

1. Pressiona "-"  → Ativa menu
2. Pressiona "3"  → Navega para /hemograma
   (Menu desativa automaticamente)
```

### **Cenário 2: Ação contextual na página**
```
Usuário na página inicial:

1. Pressiona "1"  → Vai para módulo ECG (atalho contextual)
```

### **Cenário 3: Conflito Menu vs Contextual**
```
Situação: Página inicial tem atalho "1" para ECG
          Menu também usa "1" para Página Inicial

Comportamento:
- Sem menu ativo: "1" → ECG (contextual)
- Com menu ativo: "1" → Página Inicial (menu tem prioridade)
```

### **Cenário 4: Campo de texto**
```
Usuário digitando idade em formulário:

1. Digite "123" → aparece "123" normalmente
2. Pressione "+" → alterna mute (utilitário funciona)
3. Pressione "1" → digita "1" (contextual NÃO funciona)
```

---

## 🧩 Estrutura de Dados

### **Estado Global**
```javascript
const Estado = {
    modoMenuAtivo: false,           // Se true, teclas 0-9 = navegação
    atalhosContextuais: {},         // {tecla: {nome, acao}}
    ultimoAnuncio: ''               // Para função repetir (*)
};
```

### **Utilitários (Constante)**
```javascript
const UTILITARIOS = {
    '-': { nome: 'Menu', acao: ativarMenu },
    '/': { nome: 'Ajuda', acao: listarAjuda },
    '*': { nome: 'Repetir', acao: repetirAnuncio },
    '+': { nome: 'Mute', acao: alternarMute }
};
```

### **Menu Navegação (Constante)**
```javascript
const MENU_NAVEGACAO = {
    '1': { nome: 'Página Inicial', acao: () => navegar('/') },
    '2': { nome: 'Módulo ECG', acao: () => navegar('/ecg') },
    '3': { nome: 'Módulo Hemograma', acao: () => navegar('/hemograma') },
    '0': { nome: 'Cancelar', acao: desativarMenu }
};
```

---

## 🛡️ Validações e Segurança

### **Teclas Permitidas**
Regex: `/^[0-9\/\*\-\+\.]$/`
- Apenas: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, /, *, -, +, .
- Todas as outras teclas são **ignoradas silenciosamente**

### **Proteção em Campos de Texto**
```javascript
function ehCampoDeTexto(element) {
    return element.tagName === 'INPUT' 
        || element.tagName === 'TEXTAREA' 
        || element.isContentEditable;
}
```

- Dentro de campos: apenas **utilitários** funcionam
- Permite digitação normal de números

### **Prevenção de Conflitos**
- `preventDefault()` apenas quando atalho é executado
- Teclas sem ação → ignoradas (não previne default)
- Logs detalhados no console para debug

---

## 📝 API Pública

### **registrarAtalhos(atalhos)**
```javascript
// Registra atalhos para a página atual
registrarAtalhos({
    '1': { nome: 'Ação 1', acao: () => console.log('Executou 1') },
    '2': { nome: 'Ação 2', acao: () => alert('Ação 2') }
});
```

### **salvarUltimoAnuncio(texto)**
```javascript
// Salva texto para repetir com *
salvarUltimoAnuncio('Bem-vindo ao sistema');
```

### **inicializarAtalhos()**
```javascript
// Inicializa sistema (chamado automaticamente)
// Registra listener keydown no document
inicializarAtalhos();
```

---

## 🐛 Debug

### **Console Logs**
```javascript
🔑 Tecla: "1" | Menu: false | Contexto: NORMAL
📄 Executando contextual: Módulo ECG

🔑 Tecla: "-" | Menu: false | Contexto: NORMAL
🛠️ Executando utilitário: Menu

🔑 Tecla: "1" | Menu: true | Contexto: NORMAL
📂 Executando menu: Página Inicial
```

### **Verificar Estado**
```javascript
// No console do navegador:
Estado.modoMenuAtivo        // true/false
Estado.atalhosContextuais   // {1: {...}, 2: {...}}
Estado.ultimoAnuncio        // "último texto anunciado"
```

---

## ✅ Vantagens desta Arquitetura

1. **Clara Separação de Responsabilidades**
   - Utilitários: sempre disponíveis
   - Menu: navegação global
   - Contextuais: ações da página

2. **Hierarquia Explícita**
   - Ordem de prioridade bem definida
   - Não há ambiguidade

3. **Fácil Manutenção**
   - Cada camada independente
   - Fácil adicionar novos atalhos

4. **Debug Facilitado**
   - Logs claros e informativos
   - Estado centralizado

5. **Segurança**
   - Validação rigorosa
   - Proteção em campos de texto

6. **Extensível**
   - Fácil adicionar novos utilitários
   - Contextuais flexíveis por página
