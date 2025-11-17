# Sistema Médico de Análisis - Guía de Instalación para Windows

## 📋 Requisitos Previos

- **Windows 10/11** (o Windows Server 2016+)
- **Python 3.8 o superior** instalado
- **Conexión a Internet** (para instalación de dependencias)

---

## 🚀 Instalación Rápida

### Paso 1: Instalar Python

1. Descargue Python desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, **marque la opción "Add Python to PATH"**
3. Complete la instalación

### Paso 2: Verificar Python

Abra el **Símbolo del sistema** (cmd) y ejecute:

```cmd
python --version
```

Debería ver algo como: `Python 3.11.x`

### Paso 3: Instalar Dependencias

En el directorio del proyecto, ejecute:

```cmd
pip install -r requirements.txt
```

Esto instalará:
- Flask 3.0.0 (servidor web)
- gTTS 2.5.0 (síntesis de voz)
- Pygame 2.5.2 (reproducción de audio)
- OpenAI 2.7.2 (análisis de imágenes)
- Pillow 12.0.0 (procesamiento de imágenes)
- Matplotlib 3.8.2 (generación de gráficos ECG)
- Y otras dependencias

---

## ▶️ Iniciar el Sistema

### Método 1: Ejecutable Batch (Recomendado)

Haga doble clic en:

```
iniciar_sistema.bat
```

El script:
- ✅ Verificará que Python esté instalado
- ✅ Verificará las dependencias
- ✅ Iniciará el servidor automáticamente
- ✅ Mostrará la URL de acceso

### Método 2: Línea de Comandos

Abra el **Símbolo del sistema** en el directorio del proyecto y ejecute:

```cmd
python app.py
```

---

## 🌐 Acceder al Sistema

Después de iniciar, abra su navegador en:

```
http://localhost:5000
```

### Acceso desde otros dispositivos (red local)

1. Obtenga la IP de su computadora:
   ```cmd
   ipconfig
   ```
   Busque "Dirección IPv4" (ejemplo: 192.168.1.100)

2. En otros dispositivos de la red, acceda:
   ```
   http://192.168.1.100:5000
   ```

---

## ⚙️ Configuración (Opcional)

### API de OpenAI (para análisis de imágenes)

Si desea usar la funcionalidad de análisis de imágenes ECG:

1. Obtenga una clave API en [platform.openai.com](https://platform.openai.com)

2. Edite `iniciar_sistema.bat` y descomente la línea:
   ```batch
   REM set OPENAI_API_KEY=tu_clave_api_aqui
   ```
   
   Cambie a:
   ```batch
   set OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. O cree un archivo `.env` en el directorio del proyecto:
   ```
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## ⌨️ Atajos de Teclado (Numpad)

El sistema tiene navegación completa por teclado:

| Tecla | Acción |
|-------|--------|
| **0** | Ir a Página Principal |
| **1** | Análisis ECG (datos) |
| **2** | Resultados ECG |
| **3** | Hub de Hemogramas |
| **4** | Análisis de Hemograma |
| **5** | Resultados de Hemograma |
| **/** | Ayuda de atajos |
| **\*** | Repetir último anuncio |
| **+** | Silenciar/Activar audio |

---

## 🛑 Detener el Sistema

Presione **Ctrl+C** en la ventana del símbolo del sistema.

---

## 🔧 Solución de Problemas

### Error: "Python no encontrado"

**Solución**: Asegúrese de que Python esté en el PATH del sistema:
1. Busque "Variables de entorno" en Windows
2. Edite la variable PATH
3. Agregue la ruta de instalación de Python (ej: `C:\Python311\`)

### Error: "pip no reconocido"

**Solución**: Use `python -m pip` en lugar de solo `pip`:
```cmd
python -m pip install -r requirements.txt
```

### Error: "Puerto 5000 en uso"

**Solución**: Otro programa está usando el puerto. Opciones:
1. Cierre la aplicación que usa el puerto 5000
2. O edite `app.py` y cambie el puerto:
   ```python
   app.run(debug=config.DEBUG, host='0.0.0.0', port=5001)
   ```

### Audio no funciona

**Solución**: 
1. Verifique que pygame esté instalado:
   ```cmd
   python -c "import pygame"
   ```
2. Reinstale pygame:
   ```cmd
   pip uninstall pygame
   pip install pygame
   ```

### Sin acceso desde otros dispositivos

**Solución**:
1. Verifique el firewall de Windows
2. Agregue una regla para permitir el puerto 5000
3. Asegúrese de que todos los dispositivos estén en la misma red

---

## 📁 Estructura del Proyecto

```
ecg_laudo_system/
├── iniciar_sistema.bat     ← Ejecutar esto para iniciar
├── app.py                   ← Aplicación principal Flask
├── config.py                ← Configuraciones
├── requirements.txt         ← Dependencias Python
├── data/                    ← Datos de ejemplos
├── models/                  ← Lógica de análisis
├── routes/                  ← Rutas de la aplicación
├── services/                ← Servicios (audio, visión, etc.)
├── static/                  ← Archivos estáticos (CSS, JS)
│   ├── audio/              ← Audios generados
│   ├── css/                ← Estilos
│   ├── js/                 ← JavaScript
│   └── ecg_images/         ← Imágenes ECG generadas
└── templates/               ← Plantillas HTML
```

---

## 📞 Soporte

Para problemas o preguntas:
- Revise los logs en la ventana del símbolo del sistema
- Consulte la documentación en los archivos .md del proyecto
- Verifique que todas las dependencias estén instaladas correctamente

---

## 🔄 Actualización

Para actualizar el sistema:

```cmd
git pull origin dev
pip install -r requirements.txt --upgrade
```

---

## ⚠️ Notas Importantes

1. **Seguridad**: No exponga este servidor directamente a Internet sin configurar autenticación y HTTPS
2. **Producción**: Para uso en producción, use un servidor WSGI como Waitress o Gunicorn
3. **Respaldo**: Mantenga copias de seguridad de sus datos y configuraciones personalizadas
4. **Actualizaciones**: Verifique periódicamente las actualizaciones de dependencias de seguridad

---

## ✅ Sistema Listo

¡El sistema está listo para usar! Acceda desde su navegador y comience a analizar ECGs y hemogramas con total accesibilidad.
