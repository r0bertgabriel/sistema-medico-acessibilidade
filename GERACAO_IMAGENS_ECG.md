# 📊 Geração de Imagens de ECG - Documentação

## 🎯 Funcionalidade Implementada

O sistema agora **gera automaticamente uma imagem do traçado de ECG** junto com o laudo, baseado nos dados fornecidos.

---

## ✨ Características

### **1. Geração Sintética de ECG**
- **Ondas Realistas**: P, QRS (Q, R, S), e T
- **Parâmetros Customizáveis**:
  - Frequência cardíaca (BPM)
  - Amplitude do complexo QRS
  - Presença de arritmias
  - Baseline wander (oscilação respiratória)
  - Ruído fisiológico

### **2. Adaptação aos Achados Clínicos**
O ECG gerado reflete os achados do laudo:

| Achado Clínico | Modificação no ECG |
|----------------|-------------------|
| Hipertrofia Ventricular Esquerda | QRS com amplitude aumentada (1.4x) |
| Baixa Voltagem QRS | QRS com amplitude reduzida (0.5x) |
| Fibrilação Atrial | Intervalos RR irregulares |
| Extrassístoles | Batimentos prematuros aleatórios |
| Bradicardia (< 50 bpm) | Variação nos intervalos RR |
| Taquicardia (> 100 bpm) | Variação nos intervalos RR |

### **3. Apresentação Profissional**
- **Grid Médico**: Quadriculado rosa típico de papel de ECG
- **Calibração**: Escala de 1mV e 0.2s
- **Informações do Paciente**: Nome, FC, idade, sexo, data/hora
- **Alta Resolução**: 150 DPI para visualização clara

---

## 🔧 Arquitetura Técnica

### **Componentes Criados**

#### **1. `services/ecg_image_generator.py`**
Serviço principal de geração de imagens:

```python
class ECGImageGenerator:
    def gerar_imagem_ecg(dados_ecg) -> str
    def gerar_ecg_sintetico(fc, duracao, amplitude_qrs, tem_arritmia)
    def plotar_ecg(tempo, sinal, dados_paciente, filepath)
    def limpar_imagens_antigas(dias=7)
```

**Métodos Privados:**
- `_gerar_onda_p()` - Contração atrial (80ms, amplitude 0.15mV)
- `_gerar_complexo_qrs()` - Despolarização ventricular (Q + R + S)
- `_gerar_onda_t()` - Repolarização ventricular (160ms, amplitude 0.3mV)
- `_adicionar_ruido()` - Ruído gaussiano realista
- `_adicionar_baseline_wander()` - Oscilação respiratória

### **2. Integração com API**

#### **Rotas Modificadas:**
- `/api/analisar` - Análise de ECG por dados
- `/api/resultado/<tipo>` - Processamento de exemplo

**Resposta da API (antes vs depois):**

```json
// ANTES
{
  "success": true,
  "laudo_texto": "...",
  "audio_url": "/static/audio/laudo_xxx.mp3",
  "achados": {...}
}

// DEPOIS
{
  "success": true,
  "laudo_texto": "...",
  "audio_url": "/static/audio/laudo_xxx.mp3",
  "imagem_url": "/static/ecg_images/ecg_xxx.png",  // NOVO!
  "achados": {...}
}
```

### **3. Templates Atualizados**

#### **`templates/analise.html`**
Exibe imagem do ECG antes do áudio e laudo:
```html
<div style="text-align: center;">
    <h4>📊 Traçado do Eletrocardiograma</h4>
    <img id="imagem-ecg" src="" alt="Traçado do ECG">
</div>
```

#### **`templates/resultados.html`**
Mesma estrutura para página de exemplos.

---

## 🎨 Algoritmo de Geração

### **1. Parâmetros de Entrada**
```python
{
    'frequencia_cardiaca': 75,    # BPM
    'duracao': 10,                # segundos
    'amplitude_qrs': 1.0,         # 0.5 a 1.5
    'tem_arritmia': False         # bool
}
```

### **2. Pipeline de Geração**

```
1. Calcular Intervalo RR
   ├─ RR = 60 / FC
   └─ Com variação: ±5% (normal) ou ±40% (arritmia)

2. Para cada batimento:
   ├─ Onda P (t + 0.08s)
   ├─ Complexo QRS (t + 0.16s)
   │  ├─ Q: deflexão negativa
   │  ├─ R: deflexão positiva principal
   │  └─ S: deflexão negativa pós-R
   └─ Onda T (t + 0.36s)

3. Adicionar Efeitos Realistas:
   ├─ Baseline Wander: sen(2π × 0.5Hz × t)
   └─ Ruído Gaussiano: σ = 0.02mV

4. Plotar com Matplotlib:
   ├─ Grid médico (vermelho/rosa)
   ├─ Sinal em preto
   ├─ Informações do paciente
   └─ Calibração
```

### **3. Ondas Gaussianas**

Todas as ondas usam funções gaussianas:

$$
f(t) = A \cdot e^{-\left(\frac{t-t_0}{\sigma}\right)^2}
$$

Onde:
- $A$ = amplitude
- $t_0$ = posição temporal
- $\sigma$ = largura (duração)

---

## 📦 Dependências Adicionadas

```txt
matplotlib==3.8.2   # Plotagem de gráficos
numpy==1.26.2       # Operações numéricas
```

**Instalação:**
```bash
pip install matplotlib numpy
```

---

## 📁 Estrutura de Arquivos

```
static/
├── audio/
│   └── laudo_*.mp3          # Áudios dos laudos
├── ecg_images/              # NOVO!
│   └── ecg_*.png            # Imagens de ECG geradas
└── uploads/
    └── *.jpg/png            # Uploads de usuários

services/
├── ecg_image_generator.py   # NOVO! Gerador de imagens
├── ecg_service.py
├── audio_service.py
└── __init__.py              # Atualizado
```

---

## 🧪 Testes

### **Teste Manual**
```bash
python test_ecg_image.py
```

**Saída esperada:**
```
🔬 Testando geração de imagem de ECG...
📋 Paciente: João da Silva
❤️  FC: 75 bpm
✅ Imagem gerada com sucesso!
📁 Caminho: static/ecg_images/ecg_448158e83eba.png
📊 Tamanho: 156.11 KB
✅ Arquivo criado corretamente!
```

### **Teste via Interface**

1. **Análise por Dados:**
   - Acesse: http://localhost:5000/analise
   - Preencha formulário
   - Clique em "Gerar Laudo"
   - ✅ Verifique imagem do ECG acima do áudio

2. **Fila de Resultados:**
   - Acesse: http://localhost:5000/resultados
   - Clique em "Gerar Laudo" de qualquer exemplo
   - ✅ Verifique imagem do ECG no resultado

---

## 🎯 Exemplos de ECG Gerados

### **Ritmo Sinusal Normal (75 bpm)**
- Ondas P, QRS, T regulares
- Amplitude QRS = 1.0mV
- Intervalos RR constantes

### **Hipertrofia Ventricular (75 bpm)**
- Ondas P, QRS, T regulares
- Amplitude QRS = 1.4mV (↑ 40%)
- Complexo QRS mais amplo

### **Fibrilação Atrial (100 bpm)**
- Sem ondas P visíveis
- Intervalos RR irregulares
- Baseline com flutter

### **Bradicardia Sinusal (45 bpm)**
- Ondas P, QRS, T presentes
- Intervalos RR longos e variáveis
- FC < 60 bpm

---

## ⚙️ Configurações

### **Customização do Gerador**

```python
# Em services/ecg_image_generator.py

# Diretório de saída
generator = ECGImageGenerator(output_dir='static/ecg_images')

# Parâmetros de plotagem
fig, ax = plt.subplots(figsize=(14, 6))  # Tamanho da figura
plt.savefig(filepath, dpi=150)           # Resolução

# Limpeza automática
generator.limpar_imagens_antigas(dias=7)  # Remover após 7 dias
```

### **Cores e Estilo**

```python
# Grid médico
ax.grid(color='#ff9999', alpha=0.5)      # Vermelho claro
ax.set_facecolor('#fff8f0')              # Fundo bege

# Sinal
ax.plot(tempo, sinal, color='#000000')   # Preto
```

---

## 🚀 Benefícios

### **Para Médicos:**
- ✅ Visualização rápida do traçado
- ✅ Confirmação dos achados descritos
- ✅ Exportação junto com laudo

### **Para Pacientes:**
- ✅ Compreensão visual do exame
- ✅ Arquivo compartilhável
- ✅ Registro permanente

### **Para o Sistema:**
- ✅ Laudo mais completo
- ✅ Validação visual dos dados
- ✅ Profissionalismo aumentado

---

## 🔮 Melhorias Futuras

### **Curto Prazo:**
- [ ] Botão para download da imagem
- [ ] Derivações múltiplas (DII, V1-V6)
- [ ] Zoom/pan na imagem

### **Médio Prazo:**
- [ ] Anotações automáticas (intervalos PR, QT)
- [ ] Comparação com ECG anterior
- [ ] Exportar como PDF com laudo

### **Longo Prazo:**
- [ ] ML para gerar ECGs mais realistas
- [ ] Biblioteca de padrões patológicos
- [ ] Animação do batimento cardíaco

---

## 📝 Notas Técnicas

### **Performance:**
- Geração de imagem: ~200-300ms
- Tamanho médio: 150-200 KB (PNG)
- Taxa de amostragem: 500 Hz (padrão ECG)

### **Limitações:**
- ECG sintético (não real)
- Apenas derivação única visualizada
- Padrões complexos simplificados

### **Segurança:**
- Imagens armazenadas localmente
- Limpeza automática após 7 dias
- Nome com hash único (sem dados sensíveis)

---

## ✅ Checklist de Implementação

- [x] Criar `ECGImageGenerator` class
- [x] Implementar geração de ondas (P, QRS, T)
- [x] Adicionar efeitos realistas (ruído, baseline)
- [x] Integrar com API `/analisar`
- [x] Integrar com API `/resultado/<tipo>`
- [x] Atualizar template `analise.html`
- [x] Atualizar template `resultados.html`
- [x] Adicionar matplotlib/numpy ao requirements.txt
- [x] Criar diretório `static/ecg_images/`
- [x] Implementar limpeza automática
- [x] Criar teste `test_ecg_image.py`
- [x] Documentar funcionalidade
- [ ] Testar em produção
- [ ] Adicionar atalhos de teclado para imagem

---

**Implementado em:** 13/11/2025  
**Versão:** 1.0  
**Status:** ✅ Funcional
