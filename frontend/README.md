# PDF Tool Frontend

This is the web frontend for PDF Tool, a modern PDF manipulation app. It provides a user-friendly interface for merging PDFs, deleting pages, and more, powered by React, Vite, and Tailwind CSS.

## Features
- Merge multiple PDF files into one
- Delete specific pages or ranges from PDFs
- Drag-and-drop file upload
- Responsive, modern UI
- Connects to the backend REST API

## Getting Started

### Prerequisites
- Node.js 18+
- Backend API running (see ../backend/README.md)

### Local Development
```bash
cd frontend
npm install
npm run dev
```
- Open http://localhost:5173 in your browser (Vite's default port)
- The app uses Vite's default port for local development

### Cloud Deployment
When deployed to Cloud Run, the container runtime automatically handles port assignment and routing. No additional configuration is needed.

### Build for Production
```bash
npm run build
```
- Serve the `dist` directory with any static server
- The built files are optimized for production deployment

## Technologies Used
- React 18
- Vite
- Tailwind CSS v3
- Axios
- react-dropzone
- TypeScript

## Connecting to the Backend
- The frontend expects the backend API at http://localhost:8000 by default
- For cloud deployments, update the API URL in the components to point to your deployed backend
- You can change the API URL in the code if needed

## Troubleshooting
- If styles are missing, ensure Tailwind CSS is installed and configured as in this repo
- If you see network errors, make sure the backend is running and accessible
- If the port is already in use, Vite will automatically try the next available port

## License
MIT
