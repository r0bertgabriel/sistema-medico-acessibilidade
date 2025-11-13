# 🚀 Guia Rápido - Análise de ECG por Imagem

## Configuração Rápida (5 minutos)

### 1. Instalar Dependências

```bash
./install.sh
```

### 2. Configurar API Key da OpenAI

Edite o arquivo `.env` e adicione sua chave:

```bash
OPENAI_API_KEY=sk-proj-sua-chave-aqui
```

**Onde obter a chave?**
- Acesse: https://platform.openai.com/api-keys
- Faça login ou crie uma conta
- Clique em "Create new secret key"
- Copie a chave e cole no arquivo `.env`

### 3. Executar o Sistema

```bash
./run.sh
```

### 4. Acessar a Interface

Abra seu navegador em: **http://localhost:5000**

## 📸 Como Usar a Análise por Imagem

### Passo a Passo

1. **Acesse a página inicial** (http://localhost:5000)

2. **Clique em "📸 Análise por Imagem (IA)"**

3. **Envie sua imagem de ECG:**
   - Arraste e solte a imagem, ou
   - Clique em "📁 Selecionar Arquivo"

4. **Clique em "🔍 Analisar ECG"**

5. **Aguarde o processamento** (5-30 segundos)

6. **Visualize os resultados:**
   - Análise detalhada da IA
   - Laudo médico completo
   - Áudio do laudo (reproduz automaticamente)

### Formatos Aceitos

✅ PNG, JPG, JPEG, GIF, BMP, TIFF  
📏 Tamanho máximo: 16 MB

## 🎯 O que é Analisado?

### Dados Extraídos Automaticamente

- ✅ Frequência cardíaca
- ✅ Intervalos (PR, QRS, QT/QTc)
- ✅ Eixo elétrico
- ✅ Características das ondas (P, QRS, T)
- ✅ Alterações do segmento ST
- ✅ Bloqueios de condução
- ✅ Hipertrofias
- ✅ Sinais de isquemia
- ✅ Arritmias

### Resultado Gerado

1. **Análise da IA:** Gravidade, achados principais, diagnósticos
2. **Laudo Médico:** Texto estruturado completo
3. **Áudio:** Narração em português brasileiro acelerado

## 💡 Dicas para Melhores Resultados

### ✅ Faça

- Use imagens de alta qualidade e resolução
- Certifique-se que o ECG está bem visível
- Prefira imagens com boa iluminação
- Evite sombras ou reflexos

### ❌ Evite

- Imagens muito pequenas ou pixeladas
- ECGs parcialmente visíveis
- Imagens com muito ruído ou artefatos
- Fotos muito escuras ou claras

## 🧪 Testando via Linha de Comando

```bash
# Testar com uma imagem específica
python test_vision.py caminho/para/ecg.jpg

# Exemplo
python test_vision.py ~/Downloads/ecg_paciente.jpg
```

## 🔧 Resolução de Problemas

### Erro: "OPENAI_API_KEY não configurada"

**Solução:**
```bash
# Verifique se o arquivo .env existe
cat .env

# Configure a chave
echo 'OPENAI_API_KEY=sua-chave-aqui' > .env
```

### Erro: "Formato de arquivo não permitido"

**Solução:** Use apenas PNG, JPG, JPEG, GIF, BMP ou TIFF

### Erro: "Arquivo muito grande"

**Solução:** Reduza o tamanho da imagem (máximo 16 MB)

### Análise muito lenta

**Possíveis causas:**
- Conexão lenta com internet
- Imagem muito grande (reduza resolução)
- Problema temporário na API OpenAI

### Resultados imprecisos

**Melhorias:**
- Use imagens de melhor qualidade
- Certifique-se que o ECG completo está visível
- Verifique calibração da imagem

## 📊 Custos

Cada análise consome tokens da API OpenAI:

- **Custo médio por imagem:** $0.01 - $0.05 USD
- **Depende de:** Resolução da imagem e complexidade

**Dica:** Configure limites de gasto em sua conta OpenAI

## 🔒 Segurança

- ✅ Imagens são processadas temporariamente
- ✅ Arquivos são excluídos após análise
- ✅ Comunicação criptografada (HTTPS)
- ✅ Não armazenamos dados permanentemente

## 📱 Usando via API REST

### Exemplo com curl

```bash
curl -X POST http://localhost:5000/api/analisar_imagem \
  -F "imagem=@/caminho/para/ecg.jpg"
```

### Exemplo com Python

```python
import requests

url = 'http://localhost:5000/api/analisar_imagem'
files = {'imagem': open('ecg.jpg', 'rb')}

response = requests.post(url, files=files)
resultado = response.json()

if resultado['success']:
    print("Laudo:", resultado['laudo_texto'])
    print("Áudio:", resultado['audio_url'])
else:
    print("Erro:", resultado['error'])
```

## ⚠️ Avisos Importantes

1. **Uso Médico:** Esta é uma ferramenta auxiliar, não substitui avaliação profissional
2. **Validação:** Sempre revise os resultados da IA
3. **Privacidade:** Não envie dados reais de pacientes em ambiente de teste
4. **Custos:** Monitore uso da API OpenAI para evitar cobranças inesperadas

## 📚 Documentação Completa

Para mais detalhes, veja:
- [ANALISE_POR_IMAGEM.md](ANALISE_POR_IMAGEM.md) - Documentação técnica completa
- [README.md](README.md) - Documentação geral do sistema

## 🆘 Suporte

**Problemas?** Verifique:
1. Variável OPENAI_API_KEY configurada corretamente
2. Créditos disponíveis na conta OpenAI
3. Formato e tamanho da imagem
4. Conexão com internet

---

**Versão:** 2.0 com GPT-4o Vision  
**Última atualização:** Novembro 2024
