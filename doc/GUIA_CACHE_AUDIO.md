# 🎤 Guia Rápido - Sistema de Cache de Áudio

## ⚡ Início Rápido

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Pré-gerar Áudios (Recomendado)
```bash
python pre_gerar_audios.py
```

Isso irá:
- ✅ Gerar áudios de todos os exemplos de ECG
- ✅ Gerar áudios de todos os exemplos de Hemograma
- ✅ Salvar no cache para reutilização
- ⏱️ Leva ~1-2 minutos

### 3. Iniciar o Sistema
```bash
python app.py
```

### 4. Testar
Acesse: `http://localhost:5000`

---

## 🎯 O Que Mudou?

### ✨ Novo Sistema de Cache

**Antes:**
- Áudio gerado toda vez que botão era clicado
- Tempo: 3-5 segundos por análise
- Muito processamento TTS

**Depois:**
- Áudio gerado uma vez, reutilizado sempre
- Tempo: 0.1 segundos (30-50x mais rápido!)
- Usa texto COMPLETO dos laudos (não resumido)

### 📊 Texto Completo nos Áudios

Agora os áudios incluem TODO o conteúdo dos laudos:
- Dados do paciente
- Todos os parâmetros técnicos
- Achados completos
- Interpretação detalhada
- Conclusões

**Apenas remove caracteres de formatação** (`===`, `•`, `↑`, `↓`, etc.)

---

## 🧪 Como Testar

### Teste Rápido no Navegador
1. Acesse `http://localhost:5000/hemograma-resultados`
2. Clique em "Normal" 
3. Aguarde o áudio carregar (primeira vez: ~3s)
4. Clique em "Normal" novamente
5. Veja a diferença! (segunda vez: ~0.1s)

### Console do Navegador (F12)
Você verá:
```
✅ Cache HIT: hemograma_normal_a3f5c8d9.mp3
```

### Teste com Script
```bash
python test_audio_cache.py
```

---

## 📁 Estrutura do Cache

```
static/audio/
├── audio_cache_index.json          # Índice (não editar!)
├── ecg_normal_a3f5c8d9.mp3
├── ecg_iam_b7e2d4f1.mp3
├── hemograma_normal_c9a8b5e2.mp3
└── hemograma_anemia_d1f2e3a4.mp3
```

---

## 🔧 Comandos Úteis

### Limpar Todo o Cache
```bash
rm -rf static/audio/*.mp3
rm static/audio/audio_cache_index.json
python pre_gerar_audios.py
```

### Ver Estatísticas do Cache
```bash
python -c "
from services.audio_cache_service import AudioCacheService
cache = AudioCacheService()
print(cache.estatisticas_cache())
"
```

### Testar Sistema
```bash
python test_audio_cache.py
```

---

## 💡 Dicas

1. **Execute `pre_gerar_audios.py` após atualizar exemplos**
   - Sempre que modificar dados dos exemplos
   - Após git pull

2. **Cache é automático**
   - Não precisa fazer nada especial
   - Sistema verifica automaticamente

3. **Áudios são reutilizados por conteúdo**
   - Mesmo texto = mesmo áudio
   - Diferentes pacientes com mesmo resultado = mesmo áudio

4. **Logs no Console**
   - `✅ Cache HIT` = Reutilizou áudio existente
   - `❌ Cache MISS` = Gerou novo áudio
   - `🎤 Gerando novo áudio` = Criando arquivo

---

## ❓ Problemas Comuns

### "Áudio não toca"
```bash
# Verificar se áudios foram gerados
ls -lh static/audio/*.mp3

# Se não houver arquivos:
python pre_gerar_audios.py
```

### "Cache não funciona"
```bash
# Testar sistema
python test_audio_cache.py

# Se falhar, regenerar:
rm static/audio/audio_cache_index.json
python pre_gerar_audios.py
```

### "Erro ao gerar áudio"
```bash
# Verificar dependências
pip install gtts pydub

# Verificar FFmpeg (Windows)
# Baixar: https://www.gyan.dev/ffmpeg/builds/
# Adicionar ao PATH
```

---

## 📚 Documentação Completa

Para mais detalhes, veja:
- **`SISTEMA_CACHE_AUDIO.md`** - Documentação completa
- **`services/audio_cache_service.py`** - Código fonte
- **`test_audio_cache.py`** - Exemplos de uso

---

## ✅ Checklist de Verificação

Após implementação, verificar:

- [ ] `python pre_gerar_audios.py` executou sem erros
- [ ] Arquivos `.mp3` criados em `static/audio/`
- [ ] `audio_cache_index.json` existe
- [ ] `python test_audio_cache.py` passa todos os testes
- [ ] Interface web responde rápido na segunda vez
- [ ] Console mostra "Cache HIT" ao reutilizar

---

**Tudo pronto!** 🚀

O sistema agora:
- ✅ Gera áudios completos (texto todo)
- ✅ Cacheia automaticamente
- ✅ Responde 30-50x mais rápido
- ✅ Remove caracteres especiais
- ✅ Reutiliza áudios idênticos
