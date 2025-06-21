// API configuration for different environments
export const getApiBaseUrl = (): string => {
  // Check if we're running in production (Cloud Run)
  if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    // In Cloud Run, the backend service URL needs to be configured
    // This should be set as an environment variable or config
    const backendUrl = import.meta.env.VITE_BACKEND_URL || window.location.origin.replace('pdftool-frontend', 'pdftool-backend')
    return backendUrl
  }
  
  // Local development
  return 'http://localhost:8000'
}

export const API_BASE_URL = getApiBaseUrl() 