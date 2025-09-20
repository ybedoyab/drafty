#!/usr/bin/env python3
"""
Script para sincronizar variables de entorno del módulo AI local
con el archivo principal .env
"""

import os
import shutil
from pathlib import Path

def sync_ai_env():
    """Sincroniza variables de AI desde .env principal a ai/draftycrew/.env"""
    
    # Rutas de archivos
    main_env = Path(".env")
    ai_env = Path("ai/draftycrew/.env")
    
    # Verificar que existe el archivo principal
    if not main_env.exists():
        print("❌ Archivo .env principal no encontrado")
        print("   Copia env.example a .env y configura tus valores:")
        print("   cp env.example .env")
        return False
    
    # Leer variables del archivo principal
    ai_vars = {}
    with open(main_env, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                # Solo variables relacionadas con AI (con prefijo AI_)
                if key.startswith('AI_'):
                    # Convertir AI_MODEL -> MODEL, AI_OPENAI_API_KEY -> OPENAI_API_KEY, etc.
                    clean_key = key[3:]  # Remove 'AI_' prefix
                    ai_vars[clean_key] = value
                elif key in ['BACKEND_ENVIRONMENT', 'BACKEND_DEBUG', 'BACKEND_LOG_LEVEL']:
                    # También incluir variables de aplicación para el AI module
                    clean_key = key.replace('BACKEND_', '')
                    ai_vars[clean_key] = value
    
    # Crear archivo .env para AI module
    ai_env.parent.mkdir(parents=True, exist_ok=True)
    
    with open(ai_env, 'w', encoding='utf-8') as f:
        f.write("# ===========================================\n")
        f.write("# AI MODULE CONFIGURATION (LOCAL ONLY)\n")
        f.write("# ===========================================\n")
        f.write("# This file is auto-generated from main .env\n")
        f.write("# Do not edit manually - run sync-ai-env.py to update\n\n")
        
        f.write("# AI Model Configuration\n")
        for key, value in ai_vars.items():
            f.write(f"{key}={value}\n")
    
    print("✅ Variables de AI sincronizadas exitosamente")
    print(f"   Archivo actualizado: {ai_env}")
    print(f"   Variables sincronizadas: {', '.join(ai_vars.keys())}")
    
    return True

if __name__ == "__main__":
    sync_ai_env()
