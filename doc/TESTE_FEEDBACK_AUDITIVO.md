# 🧪 Guia de Teste: Feedback Auditivo

## ✅ Sistema Implementado

O sistema de feedback auditivo foi completamente reformulado com:

1. **Web Speech API**: Fala em voz alta em português (pt-BR)
2. **ARIA Live Regions**: Compatibilidade com leitores de tela
3. **Logs detalhados**: Console mostra todos os eventos
4. **Event Capture**: Captura TODOS os eventos de foco

## 🔧 Melhorias Aplicadas

### Antes ❌
- `role="status"` e `aria-live="polite"` - baixa prioridade
- Sem Web Speech API
- Event listener sem capture

### Depois ✅
- `role="alert"` e `aria-live="assertive"` - alta prioridade
- Web Speech API integrada (velocidade 1.2x)
- Event listener com `capture: true` - pega TODOS os eventos
- Função `obterLabel()` robusta que tenta 6 métodos diferentes

## 📋 Como Testar

### 1. Página de Teste Dedicada
Acesse: **http://localhost:5000/teste-acessibilidade**

Esta página tem campos específicos para testar o feedback.

### 2. Abrir Console do Navegador
- Pressione **F12** (Firefox/Chrome)
- Vá para a aba "Console"
- Você verá mensagens com:
  - ✅ Sistema de acessibilidade iniciado
  - 👁️ Foco em: [elemento]
  - 🔊 Anunciando: [texto]
  - 🔄 Mudança em: [elemento]

### 3. Testar Navegação por Teclado

#### Pressione Tab repetidamente:
1. **Link de navegação** → Deve anunciar: "Link: Ir para página inicial - Atalho: Tecla 1"
2. **Campo de texto** → Deve anunciar: "Campo: Nome - obrigatório"
3. **Campo numérico** → Deve anunciar: "Campo: Idade"
4. **Select (dropdown)** → Deve anunciar: "Lista: Gênero - opção atual: Selecione..."
5. **Checkbox** → Deve anunciar: "Caixa de seleção: Aceito os termos - desmarcado"
6. **Botão** → Deve anunciar: "Botão: Testar Botão"
7. **Textarea** → Deve anunciar: "Área de texto: Comentários"

### 4. Testar Mudanças de Valor

#### Alterar Select:
1. Foque no campo "Gênero"
2. Pressione seta para baixo
3. Selecione "Masculino"
4. Deve anunciar: "Gênero alterado para: Masculino"

#### Marcar Checkbox:
1. Foque no checkbox "Aceito os termos"
2. Pressione Espaço
3. Deve anunciar: "Aceito os termos agora está marcado"

### 5. Testar na Página de Análise
Acesse: **http://localhost:5000/analise**

Use Tab para navegar pelos campos:
- Frequência Cardíaca (bpm)
- Intervalo PR (ms)
- Complexo QRS (ms)
- Todos os outros campos

## 🎙️ O Que Você Deve Ouvir

### No Console:
```
✅ Sistema de acessibilidade iniciado
🎹 Atalhos disponíveis:
  1 - Ir para Início
  2 - Ir para Análise ECG
  3 - Ir para Fila de Resultados
👁️ Foco em: INPUT text nome
🔊 Anunciando: Campo: Nome - obrigatório
```

### No Áudio (Web Speech API):
Uma voz em português falando:
- "Campo: Nome - obrigatório"
- "Lista: Gênero - opção atual: Selecione..."
- "Botão: Testar Botão"

## 🐛 Resolução de Problemas

### Problema 1: Não ouço áudio
**Solução**: 
- Verifique se o volume do sistema está ligado
- Verifique se o navegador tem permissão para áudio
- No Firefox: `about:preferences#privacy` → Permissões → Permitir áudio

### Problema 2: Console não mostra mensagens
**Solução**:
- Recarregue a página com Ctrl+Shift+R (hard reload)
- Verifique se o console não está filtrado
- Procure por mensagens com emoji: ✅ 👁️ 🔊 🔄

### Problema 3: Tab não funciona
**Solução**:
- Certifique-se de que não está em um campo de texto
- Pressione Esc primeiro para sair de qualquer foco
- Use Shift+Tab para voltar

### Problema 4: Áudio muito rápido/lento
**Solução**:
No arquivo `base.html`, linha ~270, altere:
```javascript
utterance.rate = 1.2; // Ajuste entre 0.5 e 2.0
```

## 🔬 Verificação Técnica

### JavaScript Carregado?
No console, digite:
```javascript
typeof anunciar
```
Deve retornar: `"function"`

### Web Speech API disponível?
No console, digite:
```javascript
'speechSynthesis' in window
```
Deve retornar: `true`

### Anunciador ARIA criado?
No console, digite:
```javascript
document.querySelector('[role="alert"]')
```
Deve retornar: `<div role="alert" ...>`

### Testar manualmente:
No console, digite:
```javascript
anunciar("Teste de áudio em português")
```
Você deve ouvir a frase falada!

## 📊 Elementos Suportados

| Elemento | Anúncio | Status |
|----------|---------|--------|
| Link (`<a>`) | "Link: [texto/aria-label]" | ✅ |
| Botão (`<button>`) | "Botão: [texto]" | ✅ |
| Input text | "Campo: [label] - obrigatório" | ✅ |
| Input number | "Campo: [label] - valor atual: X" | ✅ |
| Select | "Lista: [label] - opção atual: X" | ✅ |
| Checkbox | "Caixa de seleção: [label] - marcado/desmarcado" | ✅ |
| Radio | "Opção: [label] - selecionado" | ✅ |
| Textarea | "Área de texto: [label]" | ✅ |
| Audio player | "Player de áudio - pressione espaço" | ✅ |
| Headers (H1-H6) | "Título nível X: [texto]" | ✅ |

## 🎯 Critérios de Sucesso

### Teste PASSOU se:
- [x] Console mostra "✅ Sistema de acessibilidade iniciado"
- [x] Console mostra "👁️ Foco em:" quando usa Tab
- [x] Console mostra "🔊 Anunciando:" com o texto correto
- [x] Áudio fala em português quando foca em campo
- [x] Áudio fala quando altera valor de select/checkbox
- [x] Todos os 10+ tipos de elementos são anunciados

### Teste FALHOU se:
- [ ] Console não mostra mensagens
- [ ] Áudio não toca (mas console mostra mensagens)
- [ ] Alguns campos não são anunciados

## 📞 Próximos Passos

Se tudo funcionar:
1. Teste com leitor de tela real (NVDA, JAWS, VoiceOver)
2. Ajuste velocidade se necessário
3. Personalize mensagens se desejar

Se algo não funcionar:
1. Cole o erro do console aqui
2. Informe qual campo específico não funciona
3. Informe qual navegador está usando

## 🚀 Tecnologias Usadas

- **Web Speech API**: `window.speechSynthesis`
- **ARIA Live Regions**: `role="alert"`, `aria-live="assertive"`
- **Event Capture**: `addEventListener(..., true)`
- **Portuguese TTS**: `utterance.lang = 'pt-BR'`
- **Rate**: 1.2x mais rápido que normal
