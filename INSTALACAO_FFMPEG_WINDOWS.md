# Instalação do FFmpeg no Windows

## O que é FFmpeg?

FFmpeg é uma ferramenta necessária para processar e acelerar arquivos de áudio. O sistema funcionará sem ele, mas os áudios não serão acelerados.

## Sintomas de FFmpeg não instalado

```
RuntimeWarning: Couldn't find ffprobe or avprobe - defaulting to ffprobe, but may not work
⚠️ FFmpeg não encontrado. Usando áudio sem aceleração.
```

## Opção 1: Instalação Rápida via Chocolatey (Recomendado)

Se você tem o Chocolatey instalado:

```powershell
choco install ffmpeg
```

## Opção 2: Instalação Manual

### Passo 1: Download

1. Acesse: https://www.gyan.dev/ffmpeg/builds/
2. Baixe a versão **ffmpeg-release-essentials.zip**
3. Extraia o arquivo ZIP

### Passo 2: Instalação

1. Mova a pasta extraída para `C:\ffmpeg`
2. A estrutura deve ficar assim:
   ```
   C:\ffmpeg\
   ├── bin\
   │   ├── ffmpeg.exe
   │   ├── ffplay.exe
   │   └── ffprobe.exe
   ├── doc\
   └── presets\
   ```

### Passo 3: Adicionar ao PATH

#### Via Interface Gráfica:
1. Pressione `Win + X` e selecione "Sistema"
2. Clique em "Configurações avançadas do sistema"
3. Clique em "Variáveis de Ambiente"
4. Em "Variáveis do sistema", encontre "Path" e clique em "Editar"
5. Clique em "Novo" e adicione: `C:\ffmpeg\bin`
6. Clique em "OK" em todas as janelas

#### Via PowerShell (Administrador):
```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\ffmpeg\bin", "Machine")
```

### Passo 4: Verificar Instalação

Abra um **novo** terminal (CMD ou PowerShell) e execute:

```bash
ffmpeg -version
```

Você deve ver informações sobre a versão do FFmpeg.

## Opção 3: Usar sem aceleração

Se preferir não instalar o FFmpeg, o sistema funcionará normalmente, mas os áudios serão gerados em velocidade normal (sem aceleração de 1.35x).

## Testando no Sistema

Após instalar:

1. Feche todos os terminais abertos
2. Abra um novo terminal
3. Execute o sistema novamente
4. Gere um laudo
5. Você não deve mais ver avisos sobre FFmpeg

## Problemas Comuns

### "FFmpeg não é reconhecido como comando"

- Verifique se adicionou corretamente ao PATH
- Reinicie o terminal após adicionar ao PATH
- Reinicie o computador se necessário

### "Couldn't find ffprobe"

- Certifique-se de que `ffprobe.exe` está na mesma pasta que `ffmpeg.exe`
- Verifique se o PATH aponta para a pasta `bin` do FFmpeg

### Erro de permissão ao adicionar ao PATH

- Execute o PowerShell como Administrador
- Use a opção "Variáveis do usuário" ao invés de "Variáveis do sistema"

## Alternativas no Linux

No Linux, a instalação é mais simples:

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

### Fedora:
```bash
sudo dnf install ffmpeg
```

### Arch Linux:
```bash
sudo pacman -S ffmpeg
```

## Links Úteis

- Site oficial do FFmpeg: https://ffmpeg.org/
- Builds para Windows: https://www.gyan.dev/ffmpeg/builds/
- Documentação FFmpeg: https://ffmpeg.org/documentation.html
