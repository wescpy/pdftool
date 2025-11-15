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
For cloud deployments, the frontend automatically detects the environment and constructs the backend URL:

1. **Automatic Detection**: The app detects if it's running on localhost vs. a cloud domain
2. **Backend URL Construction**: In Cloud Run, it constructs the backend URL by replacing `pdftool-frontend` with `pdftool-backend` in the service URL
3. **CORS Support**: Backend automatically allows requests from Cloud Run service URLs
4. **Environment Variable Override**: You can override the backend URL by setting the `VITE_BACKEND_URL` environment variable during the build

#### Setting Custom Backend URL (Optional)
If you need to use a different backend URL, set the environment variable during build:
```bash
VITE_BACKEND_URL=https://your-backend-service-url.com npm run build
```

### Build for Production
```bash
npm run build
```
- Serve the `dist` directory with any static server
- The built files are optimized for production deployment

### Docker Deployment
```bash
# Build the Docker image
docker build -t pdftool-frontend .

# Run the container
docker run -p 80:80 pdftool-frontend
```

**Note**: The Docker build uses `--legacy-peer-deps` to resolve React version conflicts between React 19 and testing libraries. The container serves the production build via nginx on port 80.

## Technologies Used
- React 18
- Vite
- Tailwind CSS v3
- Axios
- react-dropzone
- TypeScript

## Connecting to the Backend

### Local Development
- The frontend automatically connects to `http://localhost:8000` for local development
- Backend CORS is configured to accept requests from `http://localhost:5173`
- No additional configuration needed

### Cloud Deployment
For cloud deployments, the frontend automatically detects the environment and constructs the backend URL:

1. **Automatic Detection**: The app detects if it's running on localhost vs. a cloud domain
2. **Backend URL Construction**: In Cloud Run, it constructs the backend URL by replacing `pdftool-frontend` with `pdftool-backend` in the service URL
3. **CORS Support**: Backend automatically allows requests from Cloud Run service URLs
4. **Environment Variable Override**: You can override the backend URL by setting the `VITE_BACKEND_URL` environment variable during the build

#### Setting Custom Backend URL (Optional)
If you need to use a different backend URL, set the environment variable during build:
```bash
VITE_BACKEND_URL=https://your-backend-service-url.com npm run build
```

### Troubleshooting Backend Connection
- If you see network errors, make sure the backend is running and accessible
- For Cloud Run deployments, ensure both frontend and backend services are deployed
- Check that the backend service name follows the pattern `pdftool-backend` (or set VITE_BACKEND_URL)
- CORS errors are automatically handled for both local and cloud environments

## Troubleshooting
- If styles are missing, ensure Tailwind CSS is installed and configured as in this repo
- If the port is already in use, Vite will automatically try the next available port

## License
Apache License, Version 2.0 - see the [LICENSE](../LICENSE) file for details.
