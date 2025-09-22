# Drafty - Generador AI de Código OpenSCAD 🚀
![Logo](https://github.com/user-attachments/assets/b4f00813-73d9-4598-b179-bc2755206a76)

Proyecto para Huawei Developer Competition 2025

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
  - 🤖 Huawei Cloud ModelArts DeepSeek-R1-Distil-Qwen-32B (análisis y generación de código)
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

## 🚀 Instalación y uso

### 🐳 Opción 1: Docker (Recomendado)

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/ybedoyab/drafty.git
   cd drafty
   ```

2. **Configura las variables de entorno:**
   ```bash
   cp env.example .env
   # Edita .env con tus credenciales de DeepSeek
   ```

3. **Ejecuta con Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Accede a la aplicación:**
   - Frontend: [http://localhost:80](http://localhost:80)
   - Backend API: [http://localhost:8000](http://localhost:8000)

### 🛠️ Opción 2: Instalación manual

#### Configuración de variables de entorno

Crea un archivo `.env` en la raíz del proyecto con:
```env
# AI Configuration (Huawei Cloud ModelArts)
AI_MODEL=deepseek-r1-distil-qwen-32b_raziqt
AI_DEEPSEEK_API_KEY=tu_clave_de_huawei_modelarts_aqui
AI_DEEPSEEK_BASE_URL=https://pangu.ap-southeast1.myhuaweicloud.com/api/v2/chat/completions
AI_HF_TOKEN=tu_token_de_huggingface_aqui

# Frontend Configuration
FRONTEND_API_URL=http://localhost:8000
```

#### Backend (FastAPI)

1. Ve a la carpeta del backend:
   ```bash
   cd backend
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # En Windows
   source .venv/bin/activate  # En Linux/Mac
   ```

3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta el backend:
   ```bash
   python run.py
   ```

#### Frontend (React)

1. Ve a la carpeta del frontend:
   ```bash
   cd frontend
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

## ☁️ Despliegue en la nube

Drafty está optimizado para despliegue en **Huawei Cloud** con soporte completo para:

- **ECS (Elastic Cloud Server)**: Hosting de la aplicación
- **DDS (Document Database Service)**: Base de datos MongoDB
- **OBS (Object Storage Service)**: Almacenamiento de archivos
- **EIP (Elastic IP)**: Acceso público seguro

Para instrucciones detalladas de despliegue, consulta la documentación de configuración (disponible localmente).

---

## ℹ️ Notas importantes

- El código generado es **OpenSCAD puro**. No se visualiza en 3D dentro de la app, pero puedes verlo fácilmente en [https://ochafik.com/openscad2](https://ochafik.com/openscad2) o en el programa OpenSCAD.
- El frontend ha sido optimizado para una experiencia moderna, clara y profesional.
- El backend genera un archivo único por cada imagen subida, evitando sobrescrituras.

---

## 👨‍💻 Créditos
- Proyecto desarrollado para Huawei Developer Competition 2025
- Repositorio: [https://github.com/ybedoyab/drafty](https://github.com/ybedoyab/drafty)
- Visualizador online recomendado: [https://ochafik.com/openscad2](https://ochafik.com/openscad2)

---

### ✍️ Autores
- **Yulian Bedoya** (estudiante de Ingeniería Mecánica)
- **Marycielo Berrio Zapata** (estudiante de Ingeniería en Sistemas)
