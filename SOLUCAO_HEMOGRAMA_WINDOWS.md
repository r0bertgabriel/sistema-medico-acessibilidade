# 🔧 Guia de Solução de Problemas - Hemograma no Windows

## ❌ Problema: Botões de Hemograma não funcionam

### Sintomas
- Ao clicar nos botões de exemplo (Normal, Anemia, Leucocitose, Plaquetopenia) nada acontece
- Console mostra erros como `AbortError: The play() request was interrupted`
- Áudio toca múltiplas vezes ou não toca

### ✅ Soluções Aplicadas

#### 1. **Erro de AbortError no áudio** - CORRIGIDO
**Causa:** Múltiplas chamadas de áudio tentando tocar ao mesmo tempo

**Correção:**
- Adicionado controle de `processandoExemplo` para prevenir cliques múltiplos
- Melhorado gerenciamento de áudio com pausa e limpeza adequadas
- Adicionado delay entre operações de áudio
- Removida função `anunciar()` duplicada (agora usa apenas a global do `audio.js`)

**Arquivos modificados:**
- `templates/hemograma_resultados.html` - JavaScript melhorado
- `static/js/audio.js` - Melhor controle de áudio e prevenção de AbortError

#### 2. **Controle de estado do processamento** - IMPLEMENTADO
```javascript
let processandoExemplo = false;

async function carregarExemplo(tipo) {
    if (processandoExemplo) {
        console.log('⏳ Já existe um processamento em andamento...');
        return;
    }
    processandoExemplo = true;
    // ... código ...
}
```

#### 3. **Melhor gerenciamento de áudio** - IMPLEMENTADO
- Para áudio anterior antes de iniciar novo
- Limpa `src` do áudio para prevenir conflitos
- Adiciona tratamento de exceções em `play()`
- Usa apenas a função global `window.anunciar()` do `audio.js`

---

## 🧪 Como Testar se Está Funcionando

### Teste 1: Interface Web
1. Acesse: `http://localhost:5000/hemograma-resultados`
2. Clique em um dos botões de exemplo (ex: "Anemia")
3. Deve aparecer:
   - Loading "Analizando hemograma..."
   - Scroll automático para o final da página
   - Player de áudio com o laudo
   - Texto completo do laudo

### Teste 2: Console do Navegador (F12)
Abra o console e verifique:
```
✅ Exemplo carregado, analisando...
✅ Análise concluída
▶️ Reproduzindo áudio...
```

**NÃO deve aparecer:**
```
❌ AbortError: The play() request was interrupted
❌ Error: Failed to fetch
```

### Teste 3: Script Python
Execute o teste automatizado:
```bash
# Certifique-se que o servidor está rodando
python app.py

# Em outro terminal:
python test_hemograma_rotas.py
```

---

## 🐛 Problemas Comuns no Windows

### Problema: "Servidor não está rodando"
**Solução:**
```bash
# Verifique se o servidor está ativo:
curl http://localhost:5000

# Se não estiver, inicie:
python app.py
```

### Problema: "ModuleNotFoundError"
**Solução:**
```bash
# Instale dependências:
pip install -r requirements.txt
```

### Problema: "Áudio não toca"
**Verificações:**
1. Verifique se o botão de mute (🔊/🔇) não está ativado
2. Verifique volume do Windows
3. Abra o console (F12) e procure erros
4. Verifique se a pasta `static/audio/` existe e tem permissões

**Solução:**
```bash
# Criar diretório se não existir:
mkdir -p static/audio

# Windows:
md static\audio
```

### Problema: "CORS Error" ou "Failed to fetch"
**Causa:** Firewall ou antivírus bloqueando

**Solução:**
1. Adicione exceção no firewall para Python
2. Temporariamente desative antivírus para teste
3. Use `127.0.0.1` ao invés de `localhost`

---

## 📋 Checklist de Verificação

Antes de reportar um problema, verifique:

- [ ] Servidor está rodando (`python app.py`)
- [ ] Porta 5000 está livre (não está sendo usada por outro app)
- [ ] Dependências instaladas (`pip list | grep -E "flask|gtts|requests"`)
- [ ] Navegador atualizado (Chrome/Edge/Firefox)
- [ ] JavaScript habilitado no navegador
- [ ] Sem erros no console do navegador (F12)
- [ ] Pasta `static/audio/` existe
- [ ] Botão de mute não está ativo

---

## 🔍 Logs Úteis

### Verificar logs do Flask
```python
# No arquivo app.py, adicione:
app.config['DEBUG'] = True
```

### Verificar chamadas de rede no navegador
1. Pressione F12
2. Vá para aba "Network" / "Rede"
3. Clique no botão de exemplo
4. Verifique se as chamadas retornam 200 OK:
   - `GET /api/hemograma/exemplo/anemia`
   - `POST /api/analisar_hemograma`

### Console JavaScript Útil
```javascript
// Ver estado do áudio
console.log('Mutado:', localStorage.getItem('audioMutado'));

// Forçar unmute
localStorage.setItem('audioMutado', 'false');
window.location.reload();
```

---

## 🆘 Ainda não funciona?

Se depois de todas essas verificações ainda houver problemas:

1. **Capture evidências:**
   - Screenshot do erro no console (F12)
   - Output do terminal onde o Flask está rodando
   - Resultado do `python test_hemograma_rotas.py`

2. **Informações do sistema:**
   - Versão do Windows
   - Versão do Python (`python --version`)
   - Navegador e versão

3. **Teste básico:**
```bash
# Teste se a rota básica funciona:
curl http://localhost:5000/api/hemograma/exemplo/normal
```

Se retornar JSON com `"success": true`, o backend está OK.
O problema pode estar no frontend/JavaScript.

---

## ✅ Correções Implementadas Nesta Atualização

1. ✅ Removido `anunciar()` duplicado em `hemograma_resultados.html`
2. ✅ Adicionado controle de `processandoExemplo` para evitar cliques múltiplos
3. ✅ Melhorado `audio.js` para prevenir AbortError:
   - Limpa `src` antes de mudar áudio
   - Adiciona delay entre operações
   - Melhor tratamento de erros em `play()`
4. ✅ Usa função global `window.anunciar()` consistentemente
5. ✅ Para áudio anterior antes de iniciar novo
6. ✅ Adiciona logs detalhados para debug

**Data da atualização:** 16/11/2025
