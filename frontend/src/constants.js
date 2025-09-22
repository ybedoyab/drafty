export const TEXT = {
  app: {
    name: 'Drafty',
  },
  nav: {
    home: 'Home',
    generate: 'Generate',
  },
  landing: {
    taglinePrefix: 'Turn',
    taglineHighlight1: '3D images',
    taglineMiddle: 'into',
    taglineHighlight2: 'OpenSCAD code',
    taglineSuffix: 'with the help of AI.',
    cta: 'Generate CAD',
    rocket: '🚀',
  },
  footer: {
    competition: 'Huawei Developer Competition 2025',
    viewOnGithub: 'View project on GitHub',
  },
  generatePage: {
    title: 'Generate CAD',
    subtitle: 'Upload an image of a 3D object and get its OpenSCAD code',
    buttonIdle: 'Generate CAD',
    buttonLoading: 'Processing image...'
  },
  backendStatus: {
    unhealthyTitle: 'Backend unavailable',
    unhealthyDesc: 'Cannot connect to the backend. Ensure the server is running.',
    healthyTitle: 'Backend connected',
    healthyDesc: 'System ready to process images.'
  },
  upload: {
    title: 'Upload a 3D image',
    subtitle: 'Drag and drop here, or click to select',
    selectFile: 'Select file',
    selectedImage: 'Selected image',
    optionalDescription: 'Add optional description',
    optionalDescriptionHelp: 'Provide extra details like dimensions, materials, or specific features to improve the generated plan accuracy',
    textareaPlaceholder: 'E.g., Ramp 1 meter high and 3 meters wide, with a 15-degree slope...',
    textareaHelp: 'Describe dimensions, materials, angles, or specific features of the object'
  },
  steps: {
    title: 'Process progress',
    items: [
      { id: 1, name: 'Upload image', description: '3D image uploaded' },
      { id: 2, name: 'Analyze image', description: 'Automatic analysis' },
      { id: 3, name: 'Generate CAD', description: 'Model generation' },
      { id: 4, name: 'OpenSCAD code', description: 'CAD script generated' }
    ]
  },
  cadViewer: {
    empty: 'No CAD model to display',
    title: 'Generated OpenSCAD Code',
    download: 'Download',
    copy: 'Copy',
    copied: 'Copied!'
  },
  resultCard: {
    successTitle: 'Plan generated successfully!',
    description: 'Your DXF file is ready to download. This file contains the engineering plan generated from your image.',
    downloadDXF: 'Download DXF'
  },
  gltfViewer: {
    title: 'Generated 3D Model (GLB)',
    download: 'Download GLB'
  },
  errors: {
    processing: 'Error processing the image',
    network: 'Connection error. Make sure the backend is running.'
  }
};


