# 🩺 Sistema de Laudos de ECG com Acessibilidade

## 📋 Descrição

Sistema web desenvolvido em Python para análise automatizada de eletrocardiogramas (ECG) com foco em **acessibilidade para médicos com deficiência visual**.

O sistema gera laudos completos em formato de **texto e áudio**, permitindo total autonomia na interpretação de ECGs.

## ✨ Funcionalidades

### 🔬 Análise Automática de ECG
- Interpretação de ritmo cardíaco e frequência
- Análise de intervalos (PR, QRS, QT/QTc)
- Avaliação do eixo elétrico
- Detecção de bloqueios de condução
- Identificação de alterações de repolarização (ST/T)
- Diagnóstico de isquemia e infarto
- Detecção de sobrecargas atriais e ventriculares

### 🔊 Geração de Áudio
- Conversão automática de laudos para áudio em português brasileiro
- Narração natural e clara usando Google Text-to-Speech
- Player de áudio integrado com controles acessíveis
- Auto-reprodução para facilitar a acessibilidade

### ⌨️ Acessibilidade
- Navegação completa por teclado
- Atalhos de teclado (Alt+1, Alt+2, Alt+3)
- Alto contraste e fontes legíveis
- Compatibilidade com leitores de tela
- Elementos ARIA para melhor experiência

## 🏗️ Arquitetura do Sistema

### Módulos Principais

#### 1. **models/ecg_data.py**
Define as estruturas de dados para ECG:
- `DadosECG`: Classe principal com todos os parâmetros
- `IntervalosECG`: Intervalos PR, QRS, QT
- `OndaP`, `ComplexoQRS`, `SegmentoST`, `OndaT`: Características específicas

#### 2. **models/ecg_analyzer.py**
Motor de análise com lógica de interpretação:
- Análise de ritmo e frequência
- Avaliação de eixo elétrico
- Detecção de bloqueios
- Identificação de padrões patológicos
- Geração de diagnósticos

#### 3. **models/laudo_generator.py**
Gerador de laudos formatados:
- Laudo completo em texto estruturado
- Laudo otimizado para narração em áudio
- Formatação médica padronizada
- Conclusões e recomendações

#### 4. **audio_generator.py**
Sistema de Text-to-Speech:
- Geração de arquivos MP3
- Gerenciamento de arquivos de áudio
- Reprodução e controle
- Limpeza automática de arquivos antigos

#### 5. **app.py**
Aplicação Flask principal:
- Rotas e endpoints da API
- Integração dos módulos
- Exemplos pré-configurados
- Interface web

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone ou baixe o projeto**
```bash
cd ecg_laudo_system
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
python app.py
```

5. **Acesse no navegador**
```
http://localhost:5000
```

## 📖 Como Usar

### 1. Página Inicial
- Apresentação do sistema
- Informações sobre funcionalidades
- Atalhos de teclado

### 2. Análise de ECG
- Preencha os dados do ECG no formulário
- Campos obrigatórios: ritmo, frequência, intervalos, eixo
- Clique em "Gerar Laudo"
- O laudo será exibido em texto e reproduzido em áudio

### 3. Exemplos Pré-configurados
- ECG Normal
- Arritmia Sinusal com Sobrecarga Atrial
- Bloqueio Incompleto do Ramo Direito
- Clique no botão para gerar o laudo do exemplo

## ⌨️ Atalhos de Teclado

- `Alt + 1` - Ir para página inicial
- `Alt + 2` - Ir para análise de ECG
- `Alt + 3` - Ver exemplos pré-configurados
- `Tab` - Navegar entre elementos
- `Enter` ou `Space` - Ativar botões e links
- `Space` - Play/Pause no player de áudio
- `Setas` - Avançar/retroceder no áudio

## 🔬 Exemplos Clínicos Incluídos

### ECG Normal
- Ritmo sinusal regular, 72 bpm
- Eixo normal (50°)
- Intervalos preservados
- Sem alterações patológicas

### Arritmia Sinusal
- Ritmo sinusal irregular
- Variação de frequência (57-100 bpm)
- Onda P com aumento atrial esquerdo
- Eixo desviado para esquerda (-18°)

### Bloqueio Incompleto de Ramo Direito
- Padrão RSR' em V1-V3
- QRS alargado (0.09s)
- Alterações secundárias de repolarização
- Inversão de T em V1-V3

## 📊 API Endpoints

### `POST /api/analisar`
Analisa dados de ECG fornecidos em JSON

**Request:**
```json
{
  "nome_paciente": "João Silva",
  "ritmo": "sinusal",
  "frequencia_cardiaca": 70,
  "regularidade": "regular",
  "eixo_qrs": 60,
  "intervalos": {
    "pr": 0.16,
    "qrs": 0.08,
    "qt": 0.40,
    "qtc": 0.42
  }
}
```

**Response:**
```json
{
  "success": true,
  "laudo_texto": "...",
  "laudo_audio_texto": "...",
  "audio_url": "/static/audio/laudo_xyz.mp3",
  "achados": [...],
  "diagnosticos": [...]
}
```

### `POST /api/exemplo/{tipo}`
Processa um exemplo pré-configurado
- `tipo`: "normal", "arritmia_sinusal", "bloqueio_ramo"

### `GET /api/exemplos`
Retorna todos os exemplos disponíveis

## 🎯 Casos de Uso

### Para Médicos com Deficiência Visual
1. Navegue usando atalhos de teclado
2. Preencha os dados do ECG por teclado
3. Gere o laudo automaticamente
4. Ouça a narração completa do laudo
5. Use leitor de tela para detalhes adicionais

### Para Ensino e Treinamento
1. Explore os exemplos pré-configurados
2. Compare padrões normais e patológicos
3. Entenda a lógica de interpretação
4. Pratique com casos variados

### Para Documentação Rápida
1. Insira dados do ECG manualmente
2. Gere laudo padronizado
3. Copie o texto para prontuário
4. Salve o áudio para referência

## ⚠️ Avisos Importantes

- **Este sistema é uma ferramenta auxiliar**: Os laudos devem ser revisados por um médico cardiologista qualificado
- **Não substitui avaliação médica**: Use como suporte à decisão clínica
- **Validação necessária**: Sempre correlacione com quadro clínico do paciente
- **Casos críticos**: Isquemia e infarto requerem atenção médica imediata

## 🛠️ Tecnologias Utilizadas

- **Flask**: Framework web Python
- **gTTS**: Google Text-to-Speech
- **Pygame**: Reprodução de áudio
- **Python Dataclasses**: Estruturas de dados
- **HTML5/CSS3**: Interface responsiva
- **JavaScript**: Interatividade

## 📁 Estrutura de Diretórios

```
ecg_laudo_system/
├── app.py                    # Aplicação Flask principal
├── audio_generator.py        # Gerador de áudio
├── requirements.txt          # Dependências
├── README.md                # Documentação
├── models/
│   ├── __init__.py
│   ├── ecg_data.py          # Estruturas de dados
│   ├── ecg_analyzer.py      # Analisador de ECG
│   └── laudo_generator.py   # Gerador de laudos
├── templates/
│   ├── base.html            # Template base
│   ├── index.html           # Página inicial
│   ├── analise.html         # Formulário de análise
│   └── exemplos.html        # Página de exemplos
└── static/
    ├── audio/               # Arquivos de áudio gerados
    └── css/                 # Estilos personalizados
```

## 🤝 Contribuições

Este é um projeto de acessibilidade médica. Sugestões e melhorias são bem-vindas!

### Áreas para Contribuição
- Novos padrões de ECG
- Melhorias na interpretação
- Acessibilidade aprimorada
- Novos idiomas para narração
- Interface mobile

## 📄 Licença

Este projeto é fornecido como está, para fins educacionais e de acessibilidade.

## 👨‍⚕️ Créditos

Sistema desenvolvido com base em diretrizes médicas estabelecidas para interpretação de ECG.

**Referências Clínicas:**
- Critérios diagnósticos padrão de ECG
- Diretrizes de cardiologia brasileiras e internacionais
- Padrões de interpretação eletrocardiográfica

---

**Desenvolvido para acessibilidade médica** 🩺❤️

Para dúvidas ou suporte, consulte a documentação ou entre em contato.
