import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'

interface FileWithPreview extends File {
  preview?: string
}

const API_BASE_URL = 'http://localhost:8000'

export default function DeletePages() {
  const [file, setFile] = useState<FileWithPreview | null>(null)
  const [pages, setPages] = useState<string>('')
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0])
      setError(null)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1
  })

  const handleDeletePages = async () => {
    if (!file) {
      setError('Please select a PDF file')
      return
    }

    if (!pages.trim()) {
      setError('Please specify pages to delete')
      return
    }

    setIsUploading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('pages', pages)

    try {
      const response = await axios.post(`${API_BASE_URL}/delete-pages`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'blob'
      })

      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'modified.pdf')
      document.body.appendChild(link)
      link.click()
      link.remove()
      setFile(null)
      setPages('')
    } catch (err) {
      console.error('Delete pages error:', err)
      if (axios.isAxiosError(err)) {
        if (err.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          setError(`Server error: ${err.response.status} - ${err.response.statusText}`)
        } else if (err.request) {
          // The request was made but no response was received
          setError('No response from server. Please check if the backend is running.')
        } else {
          // Something happened in setting up the request that triggered an Error
          setError(`Error: ${err.message}`)
        }
      } else {
        setError('Failed to delete pages. Please try again.')
      }
    } finally {
      setIsUploading(false)
    }
  }

  const removeFile = () => {
    setFile(null)
  }

  return (
    <div>
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}`}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p className="text-blue-500">Drop the PDF file here...</p>
        ) : (
          <p className="text-gray-500">Drag and drop a PDF file here, or click to select a file</p>
        )}
      </div>

      {file && (
        <div className="mt-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-500">{file.name}</span>
            <button
              onClick={removeFile}
              className="text-red-500 hover:text-red-700"
            >
              Remove
            </button>
          </div>
          <div className="mt-4">
            <label htmlFor="pages" className="block text-sm font-medium text-gray-700">
              Pages to delete (e.g., 1,3-5,7)
            </label>
            <input
              type="text"
              id="pages"
              value={pages}
              onChange={(e) => setPages(e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              placeholder="Enter page numbers"
            />
          </div>
        </div>
      )}

      {error && (
        <div className="mt-4 text-sm text-red-600">
          {error}
        </div>
      )}

      <button
        onClick={handleDeletePages}
        disabled={isUploading || !file || !pages.trim()}
        className={`mt-4 w-full px-4 py-2 rounded-md text-white font-medium
          ${isUploading || !file || !pages.trim()
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700'
          }`}
      >
        {isUploading ? 'Processing...' : 'Delete Pages'}
      </button>
    </div>
  )
} 