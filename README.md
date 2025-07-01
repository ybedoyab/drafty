# drafty
DeepPunkAI Hackathon Project

## Estructura del proyecto

```
drafty/
├─ ai/            # Lógica de IA y agentes CrewAI
│  ├─ vision_agent.py
│  ├─ cad_agent.py
│  ├─ drawing_agent.py
│  └─ orchestrator.py
├─ backend/       # API FastAPI
│  ├─ main.py
│  └─ requirements.txt
└─ frontend/      # React + Vite
   ├─ index.html
   ├─ package.json
   ├─ vite.config.js
   └─ src/
      ├─ App.jsx
      └─ main.jsx
```

### Cómo ejecutar

1. Backend (Python)
```bash
cd drafty/backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Opción 1: Usar el archivo run.py
python run.py
# Opción 2: Usar uvicorn directamente (desde la raíz del proyecto)
cd ..  # volver a drafty/
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
2. Frontend (React)
```bash
cd drafty/frontend
npm install   # o pnpm/yarn
npm run dev   # abre http://localhost:5173
```

Sube una imagen y el sistema generará un DXF de prueba en el servidor.

### Variables de entorno (frontend)

Crea un archivo `.env` dentro de `drafty/frontend` (o `.env.production` para despliegue) con la URL de la API si el backend se aloja en dominio diferente:

```
VITE_API_URL=http://localhost:8000
```

### Despliegue en producción

1. Construye el frontend:
```bash
cd drafty/frontend
npm run build  # genera directorio dist
```
2. Arranca el backend (montará automáticamente el `dist/`):
```bash
cd drafty/backend
uvicorn main:app --host 0.0.0.0 --port 8000
```
Accede al servicio desde el navegador en http://localhost:8000.

### Frontend – Tech Stack

React + Vite + TailwindCSS + React-Router.

Durante el `npm install` se ejecutará automáticamente la instalación de Tailwind y sus peer deps (`postcss`, `autoprefixer`).
