# Frontend - Web Store

Frontend de la tienda web creado con React y Vite.

## Requisitos

- Node.js LTS: https://nodejs.org/en/download
- npm, que se instala junto con Node.js

Para verificar que Node.js y npm quedaron instalados:

```bash
node -v
npm -v
```

## Instalacion en Windows

Desde PowerShell o la terminal de VS Code:

```powershell
cd frontend
npm install
npm run dev
```

El servidor de desarrollo normalmente queda disponible en:

```text
http://localhost:5173
```

## Instalacion en macOS

Desde Terminal:

```bash
cd frontend
npm install
npm run dev
```

El servidor de desarrollo normalmente queda disponible en:

```text
http://localhost:5173
```

## Comandos utiles

Ejecutar el proyecto en modo desarrollo:

```bash
npm run dev
```

Crear una version para produccion:

```bash
npm run build
```

Previsualizar la version de produccion:

```bash
npm run preview
```

Revisar problemas de estilo o lint:

```bash
npm run lint
```

## Notas

- Si aparece un error porque el puerto `5173` ya esta ocupado, Vite puede abrir otro puerto automaticamente.
- Si instalas nuevas dependencias, ejecuta `npm install` otra vez para actualizar `node_modules`.
