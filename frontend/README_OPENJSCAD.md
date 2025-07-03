# Integración OpenJSCAD en Drafty

## ¿Qué es OpenJSCAD?

[OpenJSCAD](https://aeksco.github.io/openjscad-react/) es una librería React que permite renderizar código OpenSCAD directamente en el navegador. Esto nos permite mostrar una visualización 3D interactiva del modelo CAD generado por nuestro sistema AI.

## Instalación

Para habilitar la visualización 3D, instala la dependencia:

```bash
cd frontend
npm install openjscad-react
```

## Características

### ✅ Ventajas de OpenJSCAD
- **Renderizado en tiempo real**: Muestra el modelo 3D inmediatamente
- **Interactivo**: Rotación, zoom y pan del modelo
- **Compatible con OpenSCAD**: Interpreta código OpenSCAD estándar
- **Sin dependencias externas**: Todo se ejecuta en el navegador
- **Responsive**: Se adapta al tamaño de la pantalla

### 🔧 Funcionalidades
- Visualización 3D del modelo generado
- Controles de cámara (rotar, hacer zoom, mover)
- Renderizado en wireframe y sólido
- Exportación a formatos 3D (STL, OBJ)

## Uso

Una vez instalado, el componente `OpenJSCADViewer` automáticamente:

1. **Detecta** si OpenJSCAD está disponible
2. **Renderiza** el código OpenSCAD generado
3. **Maneja errores** de sintaxis o renderizado
4. **Muestra fallback** si no está instalado

## Ejemplo de Código OpenSCAD

El sistema AI genera código como este:

```openscad
// Ejemplo de código generado
cube([10, 10, 10]);
translate([15, 0, 0]) {
    cylinder(h=10, r=5);
}
```

OpenJSCAD lo renderiza automáticamente en 3D.

## Configuración Avanzada

### Personalización del Renderer

Puedes personalizar el renderer modificando el componente:

```jsx
<OpenJSCAD 
  script={cadScript}
  style={{ width: '100%', height: '400px' }}
  options={{
    camera: { position: [10, 10, 10] },
    renderMode: 'wireframe', // o 'solid'
    backgroundColor: '#000000'
  }}
  onError={(error) => console.error(error)}
/>
```

### Opciones Disponibles

- `camera`: Posición y orientación de la cámara
- `renderMode`: Modo de renderizado (wireframe/solid)
- `backgroundColor`: Color de fondo
- `grid`: Mostrar/ocultar grilla
- `axes`: Mostrar/ocultar ejes de coordenadas

## Solución de Problemas

### Error: "OpenJSCAD not installed"
- Ejecuta `npm install openjscad-react` en el directorio frontend

### Error: "Invalid OpenSCAD syntax"
- El código generado por AI puede tener errores de sintaxis
- Revisa el código en el `CADScriptViewer`
- Los errores se muestran en la consola del navegador

### Rendimiento lento
- Modelos complejos pueden tardar en renderizar
- Considera simplificar el código OpenSCAD
- Usa el modo wireframe para mejor rendimiento

## Recursos Adicionales

- [Documentación OpenJSCAD](https://aeksco.github.io/openjscad-react/)
- [Sintaxis OpenSCAD](https://openscad.org/documentation.html)
- [Ejemplos OpenJSCAD](https://github.com/aeksco/openjscad-react/tree/main/examples)

## Integración con el Sistema AI

El flujo completo es:

1. **Usuario sube imagen** → Frontend
2. **Backend procesa** → AI genera código OpenSCAD
3. **Frontend recibe código** → OpenJSCAD renderiza 3D
4. **Usuario ve modelo** → Interactúa con visualización

Esto crea una experiencia completa de IA a visualización 3D. 