# 🐛 Relatório de Problemas Encontrados

## Status: 5 Problemas Identificados

---

## 🔴 PROBLEMA 1: Campos Opcionais Faltando em ECGService

**Arquivo**: `services/ecg_service.py`  
**Função**: `_construir_dados_ecg()`  
**Severidade**: MÉDIA  

### Descrição
O método `_construir_dados_ecg()` não está passando todos os campos opcionais do modelo `DadosECG` ao criar o objeto.

### Campos Faltantes
- `bloqueio_av`
- `sobrecarga_atrial`
- `sobrecarga_ventricular`
- `isquemia`
- `infarto`
- `localizacao_isquemia`
- `paciente_id`
- `data_exame`

### Impacto
- Dados não são persistidos corretamente
- Análises incompletas podem ser geradas
- Perda de informação do paciente

### Solução
Adicionar os campos faltantes ao construir o objeto `DadosECG`.

---

## 🟡 PROBLEMA 2: Conversão Manual Verbosa DadosECG → Dict

**Arquivo**: `routes/api.py`  
**Função**: `processar_resultado()`  
**Severidade**: BAIXA (Code Smell)  

### Descrição
A função `processar_resultado()` faz uma conversão manual muito verbosa (60+ linhas) de objeto `DadosECG` para dicionário.

### Impacto
- Código duplicado e difícil de manter
- Propenso a erros quando modelo muda
- Reduz legibilidade

### Solução
- Usar `dataclasses.asdict()` 
- OU criar método `to_dict()` no modelo

---

## 🟡 PROBLEMA 3: Duplicação de Event Listeners keydown

**Arquivos**: `static/js/audio.js` e `static/js/keyboard.js`  
**Severidade**: BAIXA  

### Descrição
Há dois event listeners `keydown` separados:
1. `audio.js` (linha 196) - apenas tecla M
2. `keyboard.js` (linha 177) - todos os atalhos

### Impacto
- Processamento duplicado de eventos
- Possível conflito na tecla M
- Performance levemente impactada

### Solução
Consolidar em um único listener em `keyboard.js` e chamar `toggleMute()` quando necessário.

---

## 🟠 PROBLEMA 4: Memory Leak Potencial em Áudio

**Arquivo**: `static/js/audio.js`  
**Função**: `reproduzirProximo()`  
**Severidade**: MÉDIA  

### Descrição
Ao criar novo objeto `Audio`, os event listeners (`onended`, `onerror`) do áudio anterior não são removidos explicitamente.

### Impacto
- Memory leak ao longo do uso
- Performance degradada com o tempo
- Possível crash em sessões longas

### Solução
Armazenar referência e remover listeners antes de criar novo áudio.

---

## 🟢 PROBLEMA 5: Dependência de Ordem de Carregamento JS

**Arquivo**: `static/js/keyboard.js`  
**Funções**: `anunciarAtalhosPagina()`, `processarTecla()`  
**Severidade**: BAIXA (Já tem proteção)  

### Descrição
`keyboard.js` depende que `audio.js` seja carregado primeiro para acessar função `anunciar()`.

### Proteção Atual
```javascript
if (typeof anunciar !== 'undefined') {
    anunciar(mensagem);
}
```

### Impacto
- Já está protegido com check
- Mas poderia ser mais robusto

### Solução
Manter check atual OU usar padrão de módulos ES6.

---

## 📊 Resumo

| Problema | Severidade | Arquivo | Impacto |
|----------|-----------|---------|---------|
| Campos faltando ECGService | 🔴 MÉDIA | services/ecg_service.py | Dados incompletos |
| Conversão manual verbosa | 🟡 BAIXA | routes/api.py | Manutenibilidade |
| Duplicação keydown | 🟡 BAIXA | audio.js + keyboard.js | Performance leve |
| Memory leak áudio | 🟠 MÉDIA | audio.js | Memory + crash |
| Dependência JS | 🟢 BAIXA | keyboard.js | Já protegido |

---

## 🎯 Prioridade de Correção

### Alta Prioridade
1. ✅ PROBLEMA 1 - Campos faltando (dados incompletos)
2. ✅ PROBLEMA 4 - Memory leak (performance/estabilidade)

### Média Prioridade
3. ✅ PROBLEMA 3 - Duplicação keydown (otimização)

### Baixa Prioridade
4. ✅ PROBLEMA 2 - Conversão manual (refatoração futura)
5. ✅ PROBLEMA 5 - Dependência JS (já protegido)

---

## ✅ Ações Recomendadas

### Imediatas (Fazer Agora)
- [ ] Corrigir PROBLEMA 1 (campos faltando)
- [ ] Corrigir PROBLEMA 4 (memory leak)

### Curto Prazo (Próxima Semana)
- [ ] Corrigir PROBLEMA 3 (consolidar keydown)
- [ ] Revisar PROBLEMA 2 (usar asdict)

### Longo Prazo (Futuro)
- [ ] Implementar padrão de módulos ES6
- [ ] Adicionar testes automatizados
- [ ] Adicionar linting JavaScript

---

**Data**: 11/11/2024  
**Status**: ✅ Análise Completa  
**Próximo Passo**: Aplicar Correções
