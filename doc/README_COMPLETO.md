# Sistema de Laudos Médicos com Acessibilidade

Sistema desenvolvido para médicos com deficiência visual, oferecendo análise automática de **Eletrocardiogramas (ECG)** e **Hemogramas Completos** com geração de laudos em texto e áudio acelerado.

## 🎯 Funcionalidades Principais

### 📊 Módulo de Eletrocardiograma (ECG)

- **Análise por Dados**: Entrada manual de parâmetros do ECG
- **Análise por Imagem**: Upload de imagem de traçado ECG com análise via GPT-4o Vision
- **Interpretação Automática**: Baseada em diretrizes da AHA (American Heart Association)
- **Detecção de**:
  - Ritmo cardíaco e frequência (bradicardia, taquicardia, arritmias)
  - Intervalos PR, QRS e QT (bloqueios de condução)
  - Eixo elétrico e desvios patológicos
  - Bloqueios de ramo e fasciculares
  - Alterações de segmento ST e onda T (isquemia)
  - Ondas Q patológicas (infarto prévio)
  - Sobrecargas atriais e ventriculares
  - Localização anatômica de lesões isquêmicas

### 🩸 Módulo de Hemograma Completo

- **Análise Completa de Hemograma**:
  - **Série Vermelha (Eritrograma)**: Hemácias, Hemoglobina, Hematócrito, VCM, HCM, CHCM, RDW
  - **Série Branca (Leucograma)**: Leucócitos, Neutrófilos, Linfócitos, Monócitos, Eosinófilos, Basófilos
  - **Plaquetas**: Contagem de trombócitos
- **Valores de Referência**: Baseados em estudos do Fleury (100.000+ indivíduos brasileiros)
- **Interpretação Inteligente**:
  - Classificação de anemias (microcítica, macrocítica, normocítica)
  - Detecção de policitemia
  - Análise de leucocitose/leucopenia
  - Identificação de neutrofilia, linfocitose, eosinofilia
  - Avaliação de plaquetopenia/plaquetose
  - Sugestões diagnósticas baseadas nos achados

### 🔊 Recursos de Acessibilidade

- **Áudio Acelerado**: Todos os laudos são convertidos em áudio com velocidade 1.35x
- **Navegação por Teclado**: Atalhos contextuais para navegação rápida
- **Feedback Auditivo**: Anúncios sonoros para todas as ações
- **Interface Otimizada**: Design pensado para leitores de tela

## 🚀 Como Usar

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>

# Entre na pasta do projeto
cd ecg_laudo_system

# Instale as dependências
pip install -r requirements.txt

# Configure a chave da API OpenAI (opcional, para análise por imagem)
export OPENAI_API_KEY="sua-chave-aqui"

# Execute o sistema
python app.py
```

### Acesso

Abra o navegador em: `http://localhost:5000`

## 📋 Estrutura do Projeto

```
ecg_laudo_system/
├── models/
│   ├── ecg_analyzer.py          # Analisador de ECG
│   ├── ecg_data.py               # Estrutura de dados ECG
│   ├── hemograma_analyzer.py     # Analisador de Hemograma
│   ├── hemograma_data.py         # Estrutura de dados Hemograma
│   └── laudo_generator.py        # Gerador de laudos
├── services/
│   ├── ecg_service.py            # Serviço de ECG
│   ├── hemograma_service.py      # Serviço de Hemograma
│   ├── audio_service.py          # Geração de áudio
│   └── vision_service.py         # Análise por imagem (GPT-4o)
├── routes/
│   ├── main.py                   # Rotas de páginas
│   └── api.py                    # Rotas da API
├── templates/
│   ├── index.html                # Página inicial
│   ├── analise.html              # Análise de ECG
│   ├── hemograma.html            # Análise de Hemograma
│   └── ...
├── static/
│   ├── css/                      # Estilos
│   ├── js/                       # Scripts (acessibilidade)
│   └── audio/                    # Áudios gerados
├── data/
│   ├── ecg_examples.py           # Exemplos de ECG
│   └── hemograma_examples.py     # Exemplos de Hemograma
└── app.py                        # Aplicação principal
```

## 🔑 Atalhos de Teclado

### Página Inicial
- `1` - Análise de ECG
- `2` - Resultados de ECG
- `3` - Análise de Hemograma
- `4` - Análise de ECG por Imagem
- `-` (hífen) - Menu principal
- `H` - Ajuda (lista atalhos)

### Páginas de Análise
- `Tab` - Navegar entre campos (com feedback auditivo)
- `Enter` - Submeter formulário

## 📊 Exemplos Disponíveis

### Exemplos de ECG
- Ritmo sinusal normal
- Bradicardia sinusal
- Taquicardia sinusal
- Fibrilação atrial
- Bloqueio AV de 1º grau
- Bloqueio de ramo direito
- Infarto anterior com supra ST
- E muito mais...

### Exemplos de Hemograma
- **Normal**: Todos os parâmetros dentro da normalidade
- **Anemia Microcítica**: Sugestivo de deficiência de ferro
- **Anemia Macrocítica**: Sugestivo de deficiência de B12/folato
- **Leucocitose com Neutrofilia**: Sugestivo de infecção bacteriana
- **Plaquetopenia**: Contagem baixa de plaquetas
- **Eosinofilia**: Elevação de eosinófilos (alergia/parasitose)
- **Leucopenia**: Redução de leucócitos
- **Policitemia**: Elevação de hemácias e hemoglobina

## 🩺 Referências Clínicas

### ECG
- American Heart Association (AHA) Guidelines
- Padrões internacionais de interpretação de ECG

### Hemograma
- Valores de referência: Laboratório Fleury (Brasil)
- Estudo com 100.000+ indivíduos
- Diretrizes internacionais de hematologia
- Referências: Delboni, SciELO, Tua Saúde

## ⚠️ Aviso Importante

Este sistema é uma **ferramenta de apoio** e **NÃO substitui** a avaliação médica profissional. Os laudos gerados devem ser interpretados por médico qualificado, considerando o contexto clínico completo do paciente.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python, Flask
- **IA**: OpenAI GPT-4o (análise por imagem)
- **TTS**: gTTS (Google Text-to-Speech)
- **Frontend**: HTML, CSS, JavaScript
- **Acessibilidade**: ARIA, navegação por teclado

## 📝 Licença

Este projeto é de código aberto para fins educacionais e de acessibilidade.

## 👥 Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue ou pull request.

## 📞 Suporte

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Desenvolvido com ❤️ para promover acessibilidade na medicina**
