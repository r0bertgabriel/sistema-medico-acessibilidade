# 🎹 Sistema de Teclado Numérico (Numpad) - Guia Completo

## ✅ Sistema Implementado para Numpad Separado

O sistema agora detecta e diferencia teclas do **teclado numérico (numpad)** do teclado principal, permitindo:
- ✅ Usar numpad para **atalhos de navegação**
- ✅ Usar numpad para **digitar números** em campos
- ✅ **Alternância automática** entre modos

---

## 🎮 Modos de Operação

### 1. **Modo Normal** (Atalhos Ativos)
- Numpad aciona atalhos da página
- Teclas alfabéticas acionam atalhos (C, R, P, H, etc)
- Tecla `-` (hífen) ou `NumpadSubtract` abre menu principal

### 2. **Modo Edição** (Digitação Ativa)
- Ativado automaticamente ao pressionar número em campo numérico
- Numpad insere números no campo
- Atalhos desativados temporariamente
- Sai com `Escape` ou `Tab` (próximo campo)

---

## 🔢 Como Funciona com Campos Numéricos

### Fluxo de Uso:

```
1. Usuário navega com Tab até campo numérico
   ↓
2. Sistema anuncia: "Campo numérico: Frequência Cardíaca. Pressione qualquer número para digitar ou Tab para próximo campo."
   ↓
3. Usuário pressiona qualquer número (numpad ou teclado principal)
   ↓
4. Sistema ATIVA automaticamente Modo Edição
   ↓
5. Sistema anuncia: "Modo edição ativado"
   ↓
6. Usuário digita números livremente com numpad
   ↓
7. Usuário pressiona Tab (próximo campo) ou Escape (sair sem avançar)
   ↓
8. Sistema DESATIVA Modo Edição
   ↓
9. Sistema anuncia: "Modo edição desativado. Atalhos reativados."
   ↓
10. Atalhos voltam a funcionar
```

---

## ⌨️ Mapeamento de Teclas do Numpad

### Numpad → Atalhos (quando NÃO está em campo numérico):

| Tecla Numpad | Código | Atalho |
|--------------|--------|--------|
| `Numpad1` | NumpadDigit1 | Atalho `1` da página |
| `Numpad2` | NumpadDigit2 | Atalho `2` da página |
| `Numpad3` | NumpadDigit3 | Atalho `3` da página |
| `Numpad4` | NumpadDigit4 | Atalho `4` (se existir) |
| `Numpad5` | NumpadDigit5 | Atalho `5` (se existir) |
| `Numpad-` | NumpadSubtract | **Menu Principal** |
| `NumpadEnter` | NumpadEnter | **Enter** (gerar laudo) |

### Numpad → Digitação (quando está em campo numérico + modo edição):

| Tecla | Ação |
|-------|------|
| `Numpad0-9` | Insere o número |
| `NumpadDecimal` | Insere ponto decimal |
| `Backspace` | Apaga caractere |
| `Delete` | Apaga caractere |
| `ArrowLeft/Right` | Move cursor |
| `Tab` | Próximo campo + desativa modo edição |
| `Escape` | Sai do modo edição (mantém foco) |
| `NumpadEnter` | Confirma e vai para próximo |

---

## 🎯 Exemplos Práticos

### Exemplo 1: Navegação Pura (SEM digitar)

```
[Página: /resultados]
Usuário: Numpad1
Sistema: ⚡ Processa resultado Normal
Usuário: NumpadSubtract (-)
Sistema: 📋 Menu principal ativado
Usuário: Numpad2
Sistema: ➡️ Navegando para Análise ECG
[Redireciona para /analise]
```

### Exemplo 2: Preenchendo Formulário (/analise)

```
[Página: /analise - Formulário de ECG]

Usuário: Tab (até "Frequência Cardíaca")
Sistema: 🔊 "Campo numérico: Frequência Cardíaca. Pressione qualquer número para digitar."
Console: 📝 Campo numérico focado.

Usuário: Numpad7
Sistema: ✏️ Modo edição ATIVADO
Sistema: 🔊 "Modo edição ativado"
Campo: "7" (cursor piscando)

Usuário: Numpad5
Campo: "75" (cursor piscando)

Usuário: Tab (vai para próximo campo)
Sistema: ✅ Saiu do campo. Modo edição desativado.
Sistema: 🔊 "Modo edição desativado. Atalhos reativados."

Usuário: Numpad1
Sistema: 🔊 "Focar no primeiro campo" (atalho acionado!)
```

### Exemplo 3: Correção em Campo Numérico

```
[Em campo "Intervalo PR" com valor "150"]

Usuário: Numpad5 (quer mudar para 155)
Sistema: ✏️ Modo edição ATIVADO
Campo: "1505" (adicionou no final)

Usuário: Backspace Backspace (apaga "05")
Campo: "15"

Usuário: Numpad5 Numpad5
Campo: "1555"

Usuário: Escape (sai sem avançar)
Sistema: 🚫 Modo edição DESATIVADO
Sistema: 🔊 "Modo edição desativado. Atalhos reativados."
[Campo mantém foco mas atalhos voltam]

Usuário: Numpad1
Sistema: ⚡ Atalho "1" acionado (foca primeiro campo)
```

---

## 🐛 Console Logs para Debug

### Log Detalhado de Cada Tecla:

```javascript
🎹 Tecla: 1, Code: Numpad1, Location: 3, Tag: BODY, Type: undefined
🔢 Numpad detectado: Numpad1 → 1
⚡ Atalho acionado: 1 - Processar resultado Normal
```

### Log ao Focar Campo:

```javascript
👁️ Foco em: INPUT number frequencia_cardiaca
📝 Campo numérico focado. Pressione qualquer número para ativar modo edição.
🔊 Anunciando: Campo numérico: Frequência Cardíaca. Pressione qualquer número para digitar.
```

### Log ao Digitar:

```javascript
🎹 Tecla: 7, Code: Numpad7, Location: 3, Tag: INPUT, Type: number
✏️ Modo edição ATIVADO (detectou digitação em campo numérico)
🔊 Anunciando: Modo edição ativado
```

### Log ao Sair:

```javascript
✅ Saiu do campo numérico. Modo edição desativado.
🔊 Anunciando: Modo edição desativado. Atalhos reativados.
```

---

## 🎓 Instruções para Usuário

### Para Navegar:
1. Use **Tab** para mover entre elementos
2. Use **Numpad** para acionar atalhos (1, 2, 3, etc)
3. Use **NumpadSubtract (-)** para menu principal
4. Use **H** para ajuda

### Para Preencher Campos Numéricos:
1. Navegue até o campo com **Tab**
2. Ouça o anúncio: "Campo numérico: [nome]"
3. **Pressione qualquer número** (numpad ou teclado) para começar
4. Ouça: "Modo edição ativado"
5. Digite os números normalmente
6. Pressione **Tab** para próximo campo OU **Escape** para sair sem avançar
7. Ouça: "Modo edição desativado"

### Para Corrigir Número Já Digitado:
1. Foque no campo (Tab até ele)
2. Pressione qualquer número para ativar modo edição
3. Use **Backspace** para apagar
4. Digite novo valor
5. Pressione **Tab** ou **Escape**

---

## ⚙️ Detecção Técnica

### Como o Sistema Detecta Numpad:

```javascript
// Propriedades do evento KeyboardEvent:
event.key       // "1" (mesmo para numpad e teclado principal)
event.code      // "Numpad1" ou "Digit1" (diferencia origem!)
event.location  // 3 = numpad, 0 = teclado principal

// Sistema mapeia:
if (event.code.startsWith('Numpad')) {
    tecla = event.code.replace('Numpad', ''); // "Numpad1" → "1"
}
```

### Teclas Especiais Detectadas:

| Código | Mapeado Para |
|--------|--------------|
| `Numpad1` → `"1"` | Atalho 1 |
| `Numpad2` → `"2"` | Atalho 2 |
| `NumpadSubtract` → `"-"` | Menu |
| `NumpadEnter` → `"Enter"` | Confirmar |
| `NumpadDecimal` → `"."` | Ponto decimal |

---

## 🔧 Configurações Opcionais

### Se quiser SEMPRE bloquear atalhos em campos numéricos:

Mude em `base.html`:

```javascript
// Linha ~215
function emCampoTexto() {
    const elemento = document.activeElement;
    if (elemento.tagName === 'INPUT' && elemento.type === 'number') {
        return true; // Sempre bloqueia, sem modo edição
    }
    // ...
}
```

### Se quiser ativar modo edição com tecla específica (ex: Insert):

```javascript
// Adicione no event listener:
if (e.key === 'Insert' && elemento.tagName === 'INPUT' && elemento.type === 'number') {
    modoEdicao = !modoEdicao;
    anunciar(modoEdicao ? 'Modo edição ativado' : 'Modo edição desativado');
    return;
}
```

---

## 🎯 Resumo

**Problema Original**: Numpad não funcionava para atalhos ❌  
**Solução**: Detecção de `event.code` com mapeamento `Numpad1` → `"1"` ✅

**Problema Secundário**: Como digitar em campos numéricos se números acionam atalhos? ❌  
**Solução**: Modo Edição automático ao pressionar primeiro número ✅

**Fluxo Final**:
1. ✅ Numpad funciona para atalhos (quando fora de campo)
2. ✅ Numpad funciona para digitar (quando em campo + modo edição)
3. ✅ Transição automática e intuitiva
4. ✅ Feedback auditivo em todas as etapas
5. ✅ Escape para sair do modo edição

---

## 🧪 Testes Sugeridos

### Teste 1: Navegação com Numpad
```bash
# Acesse
http://localhost:5000/resultados

# Teste:
Numpad1  # Deve processar Normal
```

### Teste 2: Preencher Formulário
```bash
# Acesse
http://localhost:5000/analise

# Teste:
Tab Tab Tab  # Até "Frequência Cardíaca"
Numpad7      # Ativa modo edição + digita 7
Numpad5      # Digita 5 (valor: 75)
Tab          # Próximo campo
```

### Teste 3: Menu Principal com Numpad
```bash
# Em qualquer página:
NumpadSubtract (-)  # Abre menu
Numpad2             # Vai para Análise
```

---

**Data**: 11 de Novembro de 2025  
**Versão**: 3.0 (Suporte completo a Numpad)
