# PDF Tool - Google Cloud Run Deployment Guide

This guide explains how to deploy the PDF Tool application to Google Cloud Run.

## Prerequisites

1. **Google Cloud Project**: You need a Google Cloud project with billing enabled
2. **Google Cloud CLI**: Install and configure `gcloud` CLI
3. **Docker**: Ensure Docker is installed locally for testing
4. **Enable APIs**: Enable required Google Cloud APIs

## Setup

### 1. Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 2. Set Project ID

```bash
export PROJECT_ID=$(gcloud config get-value project)
echo "Using project: $PROJECT_ID"
```

### 3. Configure Docker for Google Container Registry

```bash
gcloud auth configure-docker
```

## Local Testing

### Test Backend Container

```bash
cd backend
docker build -t pdftool-backend .
docker run -p 8000:8000 pdftool-backend
```

### Test Frontend Container

```bash
cd frontend
docker build -t pdftool-frontend .
docker run -p 80:80 pdftool-frontend
```

## Deployment

### Option 1: Using Cloud Build (Recommended)

1. **Trigger the build**:
   ```bash
   gcloud builds submit --config cloudbuild.yaml
   ```

2. **Monitor the build**:
   ```bash
   gcloud builds list --limit=1
   ```

### Option 2: Manual Deployment

#### Deploy Backend

```bash
# Build and push backend image
cd backend
docker build -t gcr.io/$PROJECT_ID/pdftool-backend:latest .
docker push gcr.io/$PROJECT_ID/pdftool-backend:latest

# Deploy to Cloud Run
gcloud run deploy pdftool-backend \
  --image gcr.io/$PROJECT_ID/pdftool-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000 \
  --memory 512Mi \
  --cpu 1
```

#### Deploy Frontend

```bash
# Build and push frontend image
cd frontend
docker build -t gcr.io/$PROJECT_ID/pdftool-frontend:latest .
docker push gcr.io/$PROJECT_ID/pdftool-frontend:latest

# Deploy to Cloud Run
gcloud run deploy pdftool-frontend \
  --image gcr.io/$PROJECT_ID/pdftool-frontend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 80 \
  --memory 256Mi \
  --cpu 1
```

## Configuration

### Environment Variables

#### Backend Environment Variables
You can set environment variables for the backend service:

```bash
gcloud run services update pdftool-backend \
  --region us-central1 \
  --set-env-vars "ENVIRONMENT=production"
```

#### Frontend Configuration
The frontend requires no special environment variables for Cloud Run deployment. The container runtime automatically handles port assignment and routing.

**Automatic Backend URL Detection**: The frontend automatically detects if it's running in Cloud Run and constructs the backend URL by replacing `pdftool-frontend` with `pdftool-backend` in the service URL.

**Optional Custom Backend URL**: If you need to use a different backend URL, you can set the `VITE_BACKEND_URL` environment variable during the build process:

```bash
# Build with custom backend URL
VITE_BACKEND_URL=https://your-backend-service-url.com npm run build
```

### Backend URL Configuration

The frontend automatically handles backend URL configuration:

1. **Local Development**: Uses `http://localhost:8000`
2. **Cloud Run**: Automatically constructs the backend URL from the service name
3. **Custom URLs**: Can be overridden with `VITE_BACKEND_URL` environment variable

No manual API URL updates are needed in the React components.

### Port Configuration Summary

| Component | Local Development | Cloud Run |
|-----------|------------------|-----------|
| Frontend  | Vite's default port (5173) | Auto-assigned by Cloud Run |
| Backend   | Port 8000 | Auto-assigned by Cloud Run |

**Note**: Cloud Run automatically handles port assignment and routing, so no explicit port configuration is needed. Vite uses port 5173 by default for local development.

## Accessing Your Application

After deployment, you can access your services:

- **Frontend**: `https://pdftool-frontend-<hash>-uc.a.run.app`
- **Backend**: `https://pdftool-backend-<hash>-uc.a.run.app`

Get the URLs with:
```bash
gcloud run services list --region us-central1
```

## Monitoring and Logs

### View Logs

```bash
# Backend logs
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=pdftool-backend" --limit=50

# Frontend logs
gcloud logs read "resource.type=cloud_run_revision AND resource.labels.service_name=pdftool-frontend" --limit=50
```

### Monitor Performance

Visit the Google Cloud Console:
- Cloud Run > Services
- Select your service
- View metrics, logs, and revisions

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the backend CORS settings include your frontend URL
2. **Build Failures**: Check the Cloud Build logs for specific error messages
3. **Service Unavailable**: Verify the service is deployed and running
4. **Memory Issues**: Increase memory allocation if needed

### Useful Commands

```bash
# List all Cloud Run services
gcloud run services list

# Describe a specific service
gcloud run services describe pdftool-backend --region us-central1

# Update service configuration
gcloud run services update pdftool-backend --region us-central1 --memory 1Gi

# Delete a service
gcloud run services delete pdftool-backend --region us-central1
```

## Cost Optimization

- **Scale to Zero**: Cloud Run automatically scales to zero when not in use
- **Memory Optimization**: Start with minimal memory and increase as needed
- **Region Selection**: Choose a region close to your users for better performance
- **Concurrency**: Adjust concurrency settings based on your traffic patterns

## Security Considerations

- **HTTPS**: Cloud Run automatically provides HTTPS
- **Authentication**: Consider adding authentication for production use
- **CORS**: Configure CORS properly to restrict access
- **Environment Variables**: Use secret management for sensitive data 