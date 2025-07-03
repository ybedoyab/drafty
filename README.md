# Drafty - Generador AI de Código OpenSCAD 🚀
![Logo](https://github.com/user-attachments/assets/b4f00813-73d9-4598-b179-bc2755206a76)

Proyecto para el DeepPunkAI Hackathon

---

## 🛠️ Problema que resuelve Drafty

En ingeniería, diseño y fabricación, transformar una idea o un boceto en un modelo CAD funcional es un proceso lento y requiere experiencia técnica. Muchos usuarios no dominan OpenSCAD ni tienen habilidades avanzadas de modelado 3D, lo que limita la adopción de la fabricación digital y la personalización de piezas.

**Drafty** automatiza la generación de código OpenSCAD a partir de imágenes, permitiendo que cualquier persona pueda obtener modelos paramétricos listos para impresión 3D o fabricación, sin conocimientos avanzados de CAD.

---

## 🤖 ¿Cómo lo resuelve Drafty? (Explicación técnica)

Drafty utiliza un pipeline de **agentes inteligentes** (CrewAI) que colaboran para analizar imágenes y generar código OpenSCAD funcional:

1. **Agente Visualizador (Analyzer):**
   - 🖼️ Analiza la imagen subida por el usuario.
   - 📏 Extrae dimensiones, formas y relaciones geométricas usando visión por computadora y LLM.
   - 📝 Genera una descripción técnica precisa y estructurada del objeto.

2. **Agente Generador CAD:**
   - 🤝 Recibe la descripción técnica.
   - 📚 Consulta una base de conocimiento de mejores prácticas y patrones OpenSCAD.
   - 💻 Genera el código OpenSCAD paramétrico y lo valida automáticamente.

**Resultado:** El usuario recibe un script OpenSCAD limpio, paramétrico y funcional, listo para ser visualizado o modificado.

---

## 🧩 Stack tecnológico

- **Frontend:**
  - ⚛️ React + Vite
  - 🎨 TailwindCSS (UI moderna y responsiva)
  - 🔗 React Router DOM
- **Backend:**
  - 🐍 FastAPI (Python)
  - ⚙️ Orquestador de pipeline de IA
- **AI/Agentes:**
  - 🧠 CrewAI (orquestación multi-agente)
  - 🤖 OpenAI GPT-4o (análisis y generación de código)
  - 🛠️ Herramientas personalizadas: VisionTool, OpenSCAD Knowledge Tool, OpenSCAD Validator
- **Otros:**
  - 🟩 OpenSCAD (sintaxis y validación)
  - 👀 Visualización recomendada: [ochafik.com/openscad2](https://ochafik.com/openscad2)

---

## 🧠 ¿Cómo se usan los agentes?

1. El usuario sube una imagen y (opcionalmente) una descripción.
2. El backend ejecuta el pipeline de CrewAI:
   - El **Agente Visualizador** analiza la imagen y produce una especificación técnica.
   - El **Agente CAD** toma esa especificación, consulta la base de conocimiento y genera el código OpenSCAD.
   - El código es validado y corregido automáticamente.
3. El frontend muestra el código generado, listo para copiar, descargar o visualizar en [ochafik.com/openscad2](https://ochafik.com/openscad2).

---

## 🚦 Instalación y uso

## 🗂️ Archivos .env requeridos

### Backend (`drafty/ai/draftycrew/.env`)

Crea un archivo `.env` en la carpeta `ai/draftycrew` con:
```env
OPENAI_API_KEY=tu_clave_de_openai
```
- **OPENAI_API_KEY**: Tu clave de API de OpenAI (necesaria para que los agentes funcionen).

### Frontend (`drafty/frontend/.env`)

Crea un archivo `.env` en la carpeta `frontend` con:
```env
VITE_API_URL=http://localhost:8000
```
- **VITE_API_URL**: URL del backend (ajusta si lo corres en otro puerto o dominio).

---

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

## ℹ️ Notas importantes

- El código generado es **OpenSCAD puro**. No se visualiza en 3D dentro de la app, pero puedes verlo fácilmente en [https://ochafik.com/openscad2](https://ochafik.com/openscad2) o en el programa OpenSCAD.
- El frontend ha sido optimizado para una experiencia moderna, clara y profesional.
- El backend genera un archivo único por cada imagen subida, evitando sobrescrituras.

---

## 👨‍💻 Créditos
- Proyecto desarrollado para el DeepPunkAI Hackathon.
- Repositorio: [https://github.com/ybedoyab/drafty](https://github.com/ybedoyab/drafty)
- Visualizador online recomendado: [https://ochafik.com/openscad2](https://ochafik.com/openscad2)

---

### ✍️ Autores
- **Yulian Bedoya** (estudiante de Ingeniería Mecánica)
- **Alejandro Guaranguay** (estudiante de Especialización en Inteligencia Artificial)
