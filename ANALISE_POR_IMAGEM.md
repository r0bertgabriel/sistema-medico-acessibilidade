# Análise de ECG por Imagem com GPT-4o Vision

## 📋 Visão Geral

Esta funcionalidade permite analisar eletrocardiogramas (ECG) diretamente de imagens usando a tecnologia GPT-4o Vision da OpenAI. O sistema extrai automaticamente todos os dados do ECG a partir da imagem e gera um laudo completo em texto e áudio.

## 🚀 Como Usar

### 1. Configuração da API Key

Para usar esta funcionalidade, você precisa configurar sua chave de API da OpenAI:

```bash
# Linux/Mac
export OPENAI_API_KEY='sua-chave-api-aqui'

# Windows (PowerShell)
$env:OPENAI_API_KEY='sua-chave-api-aqui'

# Windows (CMD)
set OPENAI_API_KEY=sua-chave-api-aqui
```

Ou crie um arquivo `.env` na raiz do projeto:

```
OPENAI_API_KEY=sua-chave-api-aqui
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o Sistema

```bash
python app.py
```

### 4. Acessar a Interface

1. Abra o navegador em `http://localhost:5000`
2. Clique em "📸 Análise por Imagem (IA)"
3. Selecione ou arraste uma imagem de ECG
4. Aguarde a análise
5. Receba o laudo completo em texto e áudio

## 📸 Formatos de Imagem Suportados

- PNG
- JPG/JPEG
- GIF
- BMP
- TIFF

Tamanho máximo: 16 MB

## 🔍 O que é Analisado

O sistema GPT-4o Vision extrai e analisa:

### Dados Quantitativos
- Frequência cardíaca (bpm)
- Intervalo PR (segundos)
- Duração QRS (segundos)
- Intervalo QT e QTc (segundos)
- Eixo elétrico (graus)

### Características do Ritmo
- Tipo de ritmo (sinusal, FA, flutter, etc.)
- Regularidade
- Descrição detalhada

### Análise de Ondas
- **Onda P**: morfologia, amplitude, duração
- **Complexo QRS**: morfologia, amplitude, presença de ondas Q patológicas
- **Onda T**: polaridade, morfologia, amplitude
- **Onda U**: presença

### Segmentos
- **Segmento ST**: elevação ou depressão, derivações afetadas, magnitude

### Diagnósticos
- Hipertrofias (VE, VD, AE, AD)
- Bloqueios (AV, de ramo, hemibloqueios)
- Isquemia (localização, tipo, agudeza)
- Arritmias (extrassístoles, outras)

### Conclusão da IA
- Gravidade geral
- Principais achados
- Diagnósticos suspeitos
- Recomendações

## 🎯 Fluxo de Processamento

```
┌─────────────────┐
│  Upload Imagem  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  GPT-4o Vision  │
│  Extrai Dados   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Conversão p/   │
│  Formato Sistema│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Análise ECG    │
│  (AnalisadorECG)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Geração Laudo  │
│  (Texto + Áudio)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Apresentação   │
│  ao Usuário     │
└─────────────────┘
```

## 🔧 Arquitetura Técnica

### Novos Componentes

#### 1. `services/vision_service.py`
Serviço responsável pela comunicação com a API GPT-4o Vision:
- `encode_image()`: Converte imagem para base64
- `analisar_ecg_imagem()`: Envia imagem para análise
- `converter_para_formato_sistema()`: Converte dados para formato interno

#### 2. Endpoint `/api/analisar_imagem`
API REST para processar imagens de ECG:
- Recebe upload de arquivo
- Valida formato e tamanho
- Processa com Vision Service
- Gera laudo e áudio
- Retorna resultado completo

#### 3. Template `analise_imagem.html`
Interface web com:
- Upload por clique ou drag-and-drop
- Preview da imagem
- Exibição da análise da IA
- Player de áudio integrado
- Design acessível

### Configurações Adicionadas

```python
# config.py
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
OPENAI_MODEL = 'gpt-4o'
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
```

## 💡 Exemplos de Uso

### Via Interface Web

1. Acesse `http://localhost:5000/analise-imagem`
2. Faça upload da imagem
3. Aguarde o processamento
4. Visualize e ouça o laudo

### Via API (curl)

```bash
curl -X POST http://localhost:5000/api/analisar_imagem \
  -F "imagem=@/caminho/para/ecg.jpg"
```

### Via API (Python)

```python
import requests

url = 'http://localhost:5000/api/analisar_imagem'
files = {'imagem': open('ecg.jpg', 'rb')}

response = requests.post(url, files=files)
resultado = response.json()

print(resultado['laudo_texto'])
print(f"Áudio: {resultado['audio_url']}")
```

## 🔒 Segurança e Privacidade

- As imagens são processadas temporariamente e excluídas após análise
- A comunicação com a API OpenAI é criptografada (HTTPS)
- Não armazenamos imagens de pacientes permanentemente
- Configure limites de taxa (rate limiting) em produção

## ⚠️ Limitações

1. **Qualidade da Imagem**: Resultados dependem da qualidade e resolução da imagem
2. **Custos**: Cada análise consome tokens da API OpenAI
3. **Latência**: Análise pode levar de 5 a 30 segundos
4. **Precisão**: IA pode cometer erros - sempre revise os resultados
5. **Uso Médico**: Esta é uma ferramenta auxiliar, não substitui avaliação profissional

## 📊 Estrutura de Resposta

```json
{
  "success": true,
  "laudo_texto": "LAUDO MÉDICO...",
  "laudo_audio_texto": "Texto simplificado para áudio...",
  "audio_url": "/static/audio/laudo_xxxxx.mp3",
  "achados": [...],
  "diagnosticos": [...],
  "analise_vision": {
    "dados_quantitativos": {...},
    "ritmo": {...},
    "ondas": {...},
    "segmentos": {...},
    "hipertrofias": {...},
    "bloqueios": {...},
    "isquemia": {...},
    "conclusao": {...}
  },
  "conclusao_ia": {
    "gravidade": "alterações moderadas",
    "principais_achados": [...],
    "diagnosticos": [...],
    "recomendacoes": [...]
  }
}
```

## 🧪 Testando a Funcionalidade

### Teste Básico

1. Use uma imagem de ECG de teste
2. Verifique se todos os dados foram extraídos corretamente
3. Compare com interpretação manual
4. Valide a qualidade do áudio

### Teste de Qualidade

- Teste com diferentes resoluções
- Teste com diferentes formatos
- Teste com ECGs de diferentes complexidades
- Teste com imagens de baixa qualidade

## 🤝 Contribuindo

Para adicionar novos recursos ou melhorar a análise:

1. Modifique o prompt em `vision_service.py` para extrair mais dados
2. Atualize o método `converter_para_formato_sistema()` para mapear novos campos
3. Ajuste `AnalisadorECG` se necessário para processar novos dados
4. Atualize a interface para exibir novas informações

## 📚 Recursos Adicionais

- [Documentação GPT-4o Vision](https://platform.openai.com/docs/guides/vision)
- [Diretrizes AHA para ECG](https://www.ahajournals.org/)
- [Flask File Upload](https://flask.palletsprojects.com/en/3.0.x/patterns/fileuploads/)

## 💰 Custos Estimados

Com GPT-4o (valores aproximados):
- Por imagem: ~$0.01 - $0.05 USD
- Depende da resolução da imagem e tamanho da resposta
- Configure limites na sua conta OpenAI

## 🐛 Troubleshooting

### Erro: "OPENAI_API_KEY não configurada"
- Configure a variável de ambiente com sua chave API

### Erro: "Formato de arquivo não permitido"
- Use apenas formatos suportados (PNG, JPG, JPEG, GIF, BMP, TIFF)

### Erro: "Arquivo muito grande"
- Reduza o tamanho da imagem (máximo 16 MB)
- Comprima a imagem mantendo legibilidade

### Resultados imprecisos
- Use imagens de alta qualidade
- Certifique-se que o ECG está bem visível
- Evite imagens com muitos artefatos ou ruído

### Análise muito lenta
- Verifique sua conexão com internet
- Considere usar imagens de menor resolução
- Verifique status da API OpenAI

## 📝 Licença

Este código é parte do Sistema de Laudos ECG com Acessibilidade e segue a mesma licença do projeto principal.
