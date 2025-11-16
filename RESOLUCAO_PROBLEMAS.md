# 🔧 Resolução de Problemas - Compatibilidade Windows/Linux

## Problemas Comuns

### 1. Erro: FFmpeg não encontrado

#### Sintomas:
```
RuntimeWarning: Couldn't find ffprobe or avprobe - defaulting to ffprobe, but may not work
⚠️ FFmpeg não encontrado. Usando áudio sem aceleração.
```

#### Causa:
FFmpeg não está instalado ou não está no PATH do sistema.

#### Solução:

**Windows:**
1. Via Chocolatey (recomendado):
   ```powershell
   choco install ffmpeg
   ```

2. Manual - Veja `INSTALACAO_FFMPEG_WINDOWS.md`

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

#### Impacto:
- ✓ Sistema funciona normalmente
- ✗ Áudios não são acelerados (velocidade 1x ao invés de 1.35x)

---

### 2. Erro: PermissionError ao renomear arquivo

#### Sintomas:
```
PermissionError: [WinError 32] O arquivo já está sendo usado por outro processo: 
'static\\audio\\temp_laudo_937ad864.mp3' -> 'static\\audio\\laudo_937ad864.mp3'
```

#### Causa:
No Windows, arquivos em uso não podem ser renomeados/movidos.

#### Solução:
✓ **CORRIGIDO** - O sistema agora:
1. Remove arquivo de destino antes de mover
2. Usa método seguro com shutil se rename falhar
3. Aguarda antes de deletar arquivo temporário

Reinicie o sistema para aplicar as correções.

---

### 3. Erro: FileNotFoundError ao processar áudio

#### Sintomas:
```
FileNotFoundError: [WinError 2] O sistema não pode encontrar o arquivo especificado
```

#### Causa:
pydub tentando usar FFmpeg que não está instalado.

#### Solução:
✓ **CORRIGIDO** - O sistema agora:
1. Detecta ausência do FFmpeg
2. Exibe mensagem informativa
3. Usa áudio sem aceleração automaticamente
4. Suprime avisos do pydub

Reinicie o sistema para aplicar as correções.

---

### 4. Erro: Caracteres estranhos no terminal Windows

#### Sintomas:
Emojis ou caracteres especiais aparecem como `?` ou quadrados.

#### Causa:
Codificação do terminal Windows (CP-1252 vs UTF-8).

#### Solução:

**Temporária (sessão atual):**
```powershell
chcp 65001
```

**Permanente:**
1. Win + R → `intl.cpl`
2. Aba "Administrativo"
3. "Alterar localidade do sistema"
4. Marcar "Beta: Usar Unicode UTF-8 para suporte a idiomas mundiais"
5. Reiniciar

**Alternativa:** Use PowerShell ao invés do CMD

---

### 5. Erro: ModuleNotFoundError

#### Sintomas:
```
ModuleNotFoundError: No module named 'flask'
ModuleNotFoundError: No module named 'gtts'
```

#### Causa:
Dependências não instaladas.

#### Solução:

1. Ative o ambiente virtual (se estiver usando):
   ```bash
   # Linux/Mac
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Verifique a instalação:
   ```bash
   python verificar_dependencias.py
   ```

---

### 6. Erro: Port 5000 already in use

#### Sintomas:
```
OSError: [Errno 98] Address already in use
```

#### Causa:
Outra instância do sistema está rodando ou outro programa usa a porta 5000.

#### Solução:

**Opção 1: Parar processo existente**

Linux/Mac:
```bash
lsof -ti:5000 | xargs kill -9
```

Windows:
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Opção 2: Usar outra porta**

Edite `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Mudar de 5000 para 5001
```

---

### 7. Erro: Audio não reproduz no navegador

#### Sintomas:
Player de áudio não carrega ou não reproduz.

#### Causa:
Caminho do arquivo incorreto ou arquivo não gerado.

#### Solução:

1. Verifique se o diretório existe:
   ```bash
   ls static/audio/  # Linux/Mac
   dir static\audio\  # Windows
   ```

2. Verifique permissões:
   ```bash
   # Linux/Mac
   chmod -R 755 static/audio/
   ```

3. Limpe cache do navegador (Ctrl+Shift+Del)

4. Verifique console do navegador (F12) para erros

---

### 8. Compatibilidade de Caminhos (Windows vs Linux)

#### Problema:
Código usa `/` (Linux) mas Windows usa `\`.

#### Solução:
✓ **CORRIGIDO** - O sistema agora usa `pathlib.Path` que é multiplataforma.

```python
# Errado (específico para um sistema)
path = "static/audio/file.mp3"  # Só Linux
path = "static\\audio\\file.mp3"  # Só Windows

# Correto (multiplataforma)
from pathlib import Path
path = Path("static") / "audio" / "file.mp3"  # Windows e Linux
```

---

## Verificação do Sistema

Execute antes de usar:

**Linux/Mac:**
```bash
python verificar_dependencias.py
```

**Windows:**
```powershell
verificar_sistema_windows.bat
# ou
python verificar_dependencias.py
```

---

## Checklist de Instalação

### Requisitos Obrigatórios:
- [ ] Python 3.8+ instalado
- [ ] pip funcionando
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Estrutura de diretórios intacta

### Requisitos Opcionais:
- [ ] FFmpeg instalado (para aceleração de áudio)
- [ ] OpenAI API Key configurada (para análise por imagem - modo online)

### Testes:
- [ ] `python app.py` inicia sem erros
- [ ] Navegador abre em `http://localhost:5000`
- [ ] Gerar laudo de ECG funciona
- [ ] Gerar laudo de hemograma funciona
- [ ] Áudio é gerado e reproduz

---

## Logs e Debug

### Habilitar logs detalhados:

Edite `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Verificar logs do Flask:
Os erros aparecem no terminal onde você executou `python app.py`

### Verificar console do navegador:
Pressione F12 → aba Console

---

## Suporte

Se o problema persistir:

1. Execute: `python verificar_dependencias.py`
2. Copie a saída completa
3. Copie a mensagem de erro do terminal
4. Copie a mensagem de erro do console do navegador (F12)
5. Informe o sistema operacional e versão
6. Informe a versão do Python (`python --version`)

---

## Diferenças Windows vs Linux

| Aspecto | Windows | Linux |
|---------|---------|-------|
| Separador de caminho | `\` | `/` |
| Variável de ambiente | `set VAR=valor` | `export VAR=valor` |
| Ativar venv | `venv\Scripts\activate` | `source venv/bin/activate` |
| Linha de comando | CMD/PowerShell | bash/zsh |
| Encoding padrão | CP-1252 | UTF-8 |
| Case sensitive | Não | Sim |

**Solução:** Use sempre `pathlib.Path` e funções multiplataforma do Python.
