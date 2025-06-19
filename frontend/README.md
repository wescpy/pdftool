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

### Setup
```bash
cd frontend
npm install
npm run dev
```
- Open http://localhost:5173 in your browser.

### Build for Production
```bash
npm run build
```
- Serve the `dist` directory with any static server.

## Technologies Used
- React 18
- Vite
- Tailwind CSS v3
- Axios
- react-dropzone

## Connecting to the Backend
- The frontend expects the backend API at http://localhost:8000 by default.
- You can change the API URL in the code if needed.

## Troubleshooting
- If styles are missing, ensure Tailwind CSS is installed and configured as in this repo.
- If you see network errors, make sure the backend is running and accessible.

## License
MIT
