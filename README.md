# Drafty - Generador AI de Código OpenSCAD

Proyecto para el DeepPunkAI Hackathon

## Descripción

Drafty es un sistema inteligente que genera código OpenSCAD a partir de imágenes usando agentes de IA. El sistema cuenta con:

- **Backend FastAPI**: Recibe imágenes, ejecuta el pipeline de IA y retorna el código OpenSCAD generado.
- **Frontend React**: Permite subir imágenes, ver y descargar el código OpenSCAD generado.

## ¿Qué hace Drafty?

- Analiza imágenes de objetos 3D (por ejemplo, piezas, rampas, muebles, etc).
- Genera automáticamente el código OpenSCAD correspondiente.
- Permite copiar o descargar el código generado.
- **No incluye visualización 3D integrada** (por compatibilidad y robustez).

## ¿Cómo visualizar el código OpenSCAD?

Puedes copiar el código generado y visualizarlo en línea en:
👉 [https://ochafik.com/openscad2](https://ochafik.com/openscad2)

O abrirlo en el programa de escritorio [OpenSCAD](https://openscad.org/).

---

## Instalación y uso

### Backend (FastAPI)

1. Ve a la carpeta del backend:
   ```bash
   cd drafty/backend
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # En Windows
   ```
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta el backend:
   ```bash
   python run.py
   # o
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend (React)

1. Ve a la carpeta del frontend:
   ```bash
   cd drafty/frontend
   ```
2. Instala dependencias:
   ```bash
   npm install
   ```
3. Ejecuta el servidor de desarrollo:
   ```bash
   npm run dev
   ```
4. Abre [http://localhost:5173](http://localhost:5173) en tu navegador.

---

## Notas importantes

- El código generado es **OpenSCAD puro**. No se visualiza en 3D dentro de la app, pero puedes verlo fácilmente en [https://ochafik.com/openscad2](https://ochafik.com/openscad2) o en el programa OpenSCAD.
- El frontend ha sido optimizado para una experiencia moderna, clara y profesional.
- El backend genera un archivo único por cada imagen subida, evitando sobrescrituras.

---

## Créditos
- Proyecto desarrollado para el DeepPunkAI Hackathon.
- Repositorio: [https://github.com/ybedoyab/drafty](https://github.com/ybedoyab/drafty)
- Visualizador online recomendado: [https://ochafik.com/openscad2](https://ochafik.com/openscad2)