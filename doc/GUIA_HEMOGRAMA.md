# Guia Rápido: Módulo de Hemograma

## 📋 Visão Geral

O módulo de Hemograma Completo do sistema analisa automaticamente os três componentes principais do sangue:

1. **Série Vermelha (Eritrograma)** 🔴
2. **Série Branca (Leucograma)** ⚪
3. **Plaquetas** 🔶

## 🩸 Parâmetros Analisados

### Série Vermelha

| Parâmetro | Unidade | Homens (ref) | Mulheres (ref) | Significado |
|-----------|---------|--------------|----------------|-------------|
| Hemácias | milhões/µL | 4.32 - 5.67 | 3.83 - 4.99 | Quantidade de glóbulos vermelhos |
| Hemoglobina | g/dL | 13.3 - 16.5 | 11.7 - 14.9 | Capacidade de transporte de O₂ |
| Hematócrito | % | 39.2 - 49.0 | 35.1 - 44.1 | Volume ocupado por hemácias |
| VCM | fL | 80.0 - 100.0 | 80.0 - 100.0 | Tamanho médio das hemácias |
| HCM | pg | 27.0 - 32.0 | 27.0 - 32.0 | Hb média por hemácia |
| CHCM | g/dL | 32.0 - 36.0 | 32.0 - 36.0 | Concentração de Hb |
| RDW | % | 11.5 - 14.5 | 11.5 - 14.5 | Variação do tamanho |

### Série Branca

| Parâmetro | Unidade | Homens (ref) | Mulheres (ref) | Função |
|-----------|---------|--------------|----------------|---------|
| Leucócitos | /µL | 3650 - 8120 | 3470 - 8290 | Defesa do organismo |
| Neutrófilos | /µL | 1800 - 7000 | 1800 - 7000 | Infecções bacterianas |
| Linfócitos | /µL | 1000 - 4000 | 1000 - 4000 | Imunidade, vírus |
| Monócitos | /µL | 100 - 1000 | 100 - 1000 | Fagocitose |
| Eosinófilos | /µL | 40 - 500 | 40 - 500 | Alergias, parasitas |
| Basófilos | /µL | 10 - 100 | 10 - 100 | Reações alérgicas |

### Plaquetas

| Parâmetro | Unidade | Referência | Significado |
|-----------|---------|------------|-------------|
| Plaquetas | /µL | 150.000 - 450.000 | Coagulação sanguínea |

## 🔍 Interpretação Automática

### Anemias

**Anemia Microcítica** (VCM < 80 fL)
- Deficiência de ferro
- Talassemia
- Doença crônica

**Anemia Normocítica** (VCM 80-100 fL)
- Perda aguda de sangue
- Doença renal crônica
- Hemólise

**Anemia Macrocítica** (VCM > 100 fL)
- Deficiência de B12
- Deficiência de folato
- Alcoolismo

### Alterações Leucocitárias

**Leucocitose** (↑ Leucócitos)
- Neutrofilia → Infecção bacteriana
- Linfocitose → Infecção viral
- Eosinofilia → Alergia, parasitose
- Monocitose → Infecção crônica

**Leucopenia** (↓ Leucócitos)
- Infecção viral
- Medicamentos
- Doenças autoimunes
- Quimioterapia

### Alterações Plaquetárias

**Plaquetopenia** (< 150.000/µL)
- Risco de sangramento
- Destruição periférica
- Produção diminuída

**Plaquetose** (> 450.000/µL)
- Trombocitose reativa
- Doenças mieloproliferativas

## 💻 Como Usar o Sistema

### 1. Acesse a Página de Hemograma
```
http://localhost:5000/hemograma
```

### 2. Preencha os Dados

**Obrigatórios:**
- Nome do paciente
- Idade
- Sexo (M/F)
- Hemácias
- Hemoglobina
- Hematócrito
- Leucócitos
- Plaquetas

**Opcionais (mas recomendados):**
- VCM, HCM, CHCM, RDW
- Diferencial leucocitário completo
- Observações clínicas

### 3. Use Exemplos Prontos

**Carregar Exemplo Normal**
- Todos os parâmetros dentro da normalidade

**Carregar Exemplo Anemia**
- Anemia microcítica (deficiência de ferro)

**Carregar Exemplo Leucocitose**
- Neutrofilia (infecção bacteriana)

**Carregar Exemplo Plaquetopenia**
- Contagem baixa de plaquetas

### 4. Analise o Resultado

O sistema gera automaticamente:
- ✅ **Laudo completo** em texto formatado
- 🔊 **Áudio acelerado** (1.35x) do laudo
- 📊 **Interpretação** com achados principais
- 🎯 **Sugestões diagnósticas**
- ⚠️ **Alertas** para valores críticos

## 🔑 Atalhos de Teclado

- `Tab` - Navegar entre campos
- `Enter` - Submeter análise
- `Esc` - Limpar formulário

## 📱 API Endpoints

### Analisar Hemograma
```http
POST /api/analisar_hemograma
Content-Type: application/json

{
  "paciente": {
    "nome": "João Silva",
    "idade": 35,
    "sexo": "M",
    "data_coleta": "12/11/2025"
  },
  "serie_vermelha": {
    "hemacias": 5.0,
    "hemoglobina": 15.0,
    "hematocrito": 45.0,
    "vcm": 90.0,
    "hcm": 30.0,
    "chcm": 34.0,
    "rdw": 13.0
  },
  "serie_branca": {
    "leucocitos": 7000,
    "neutrofilos": 4000,
    "linfocitos": 2000,
    "monocitos": 500,
    "eosinofilos": 200,
    "basofilos": 50
  },
  "plaquetas": {
    "contagem": 250000
  },
  "observacoes": "Hemograma de rotina"
}
```

### Obter Exemplo
```http
GET /api/hemograma/exemplo/{tipo}
```

Tipos disponíveis:
- `normal`
- `anemia`
- `leucocitose`
- `plaquetopenia`

### Validar Dados
```http
POST /api/hemograma/validar
Content-Type: application/json
```

## ⚠️ Valores Críticos

O sistema emite alertas especiais para:

- Hemoglobina < 7.0 g/dL (anemia severa)
- Leucócitos < 1.000/µL (leucopenia severa)
- Plaquetas < 50.000/µL (risco de sangramento)
- Leucócitos > 30.000/µL (leucocitose severa)

## 📚 Referências

- **Laboratório Fleury**: Estudo com 100.000+ indivíduos
- **Diretrizes Internacionais de Hematologia**
- **Valores de referência atualizados para população brasileira**

## 🎯 Dicas de Uso

1. **Sempre preencha sexo e idade corretamente** - Os valores de referência variam
2. **Inclua VCM quando disponível** - Essencial para classificar anemias
3. **Adicione observações clínicas** - Contexto ajuda na interpretação
4. **Use áudio acelerado** - Otimizado para eficiência (1.35x)
5. **Copie o laudo** - Botão disponível após análise

## 🔄 Comparação com Exames Anteriores

Para acompanhamento longitudinal:
1. Salve laudos anteriores
2. Compare valores em série
3. Observe tendências
4. Documente evolução clínica

---

**💡 Lembre-se:** Este sistema é uma ferramenta de apoio. A interpretação final e decisão clínica devem ser feitas por médico qualificado.
