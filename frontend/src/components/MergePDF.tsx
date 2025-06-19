import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'

interface FileWithPreview extends File {
  preview?: string
}

const API_BASE_URL = 'http://localhost:8000'

export default function MergePDF() {
  const [files, setFiles] = useState<FileWithPreview[]>([])
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(prev => [...prev, ...acceptedFiles])
    setError(null)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    }
  })

  const handleMerge = async () => {
    if (files.length < 2) {
      setError('Please select at least 2 PDF files to merge')
      return
    }

    setIsUploading(true)
    setError(null)

    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })

    try {
      const response = await axios.post(`${API_BASE_URL}/merge`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'blob'
      })

      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'merged.pdf')
      document.body.appendChild(link)
      link.click()
      link.remove()
      setFiles([])
    } catch (err) {
      console.error('Merge error:', err)
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
        setError('Failed to merge PDFs. Please try again.')
      }
    } finally {
      setIsUploading(false)
    }
  }

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index))
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
          <p className="text-blue-500">Drop the PDF files here...</p>
        ) : (
          <p className="text-gray-500">Drag and drop PDF files here, or click to select files</p>
        )}
      </div>

      {files.length > 0 && (
        <div className="mt-4">
          <h4 className="text-sm font-medium text-gray-900">Selected files:</h4>
          <ul className="mt-2 divide-y divide-gray-200">
            {files.map((file, index) => (
              <li key={index} className="py-2 flex items-center justify-between">
                <span className="text-sm text-gray-500">{file.name}</span>
                <button
                  onClick={() => removeFile(index)}
                  className="text-red-500 hover:text-red-700"
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {error && (
        <div className="mt-4 text-sm text-red-600">
          {error}
        </div>
      )}

      <button
        onClick={handleMerge}
        disabled={isUploading || files.length < 2}
        className={`mt-4 w-full px-4 py-2 rounded-md text-white font-medium
          ${isUploading || files.length < 2
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700'
          }`}
      >
        {isUploading ? 'Merging...' : 'Merge PDFs'}
      </button>
    </div>
  )
} 