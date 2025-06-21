/**
 * Unit tests for the DeletePages component.
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import DeletePages from '../../src/components/DeletePages';

// Mock axios
vi.mock('axios', () => ({
  default: {
    post: vi.fn(),
  },
}));

// Mock react-dropzone
vi.mock('react-dropzone', () => ({
  useDropzone: () => ({
    getRootProps: () => ({
      onClick: vi.fn(),
    }),
    getInputProps: () => ({}),
    isDragActive: false,
    acceptedFiles: [],
  }),
}));

describe('DeletePages Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders delete pages section', () => {
    render(<DeletePages />);
    
    expect(screen.getByText('Delete Pages')).toBeInTheDocument();
    expect(screen.getByText('Remove specific pages from a PDF')).toBeInTheDocument();
  });

  it('shows drag and drop area', () => {
    render(<DeletePages />);
    
    expect(screen.getByText('Drag & drop a PDF file here, or click to select')).toBeInTheDocument();
  });

  it('shows page input when file is selected', async () => {
    const mockFile = new File(['test content'], 'test.pdf', { type: 'application/pdf' });

    // Mock useDropzone to return a file
    vi.mocked(require('react-dropzone').useDropzone).mockReturnValue({
      getRootProps: () => ({
        onClick: vi.fn(),
      }),
      getInputProps: () => ({}),
      isDragActive: false,
      acceptedFiles: [mockFile],
    });

    render(<DeletePages />);
    
    await waitFor(() => {
      expect(screen.getByLabelText('Pages to delete (e.g., 1,3-5,7)')).toBeInTheDocument();
    });
  });

  it('handles delete button click', async () => {
    const mockFile = new File(['test content'], 'test.pdf', { type: 'application/pdf' });

    const mockAxios = vi.mocked(require('axios').default);
    mockAxios.post.mockResolvedValue({
      data: new Blob(['modified pdf content'], { type: 'application/pdf' }),
      headers: { 'content-disposition': 'attachment; filename=modified.pdf' },
    });

    // Mock useDropzone to return a file
    vi.mocked(require('react-dropzone').useDropzone).mockReturnValue({
      getRootProps: () => ({
        onClick: vi.fn(),
      }),
      getInputProps: () => ({}),
      isDragActive: false,
      acceptedFiles: [mockFile],
    });

    render(<DeletePages />);
    
    const pageInput = screen.getByLabelText('Pages to delete (e.g., 1,3-5,7)');
    fireEvent.change(pageInput, { target: { value: '2,4' } });

    const deleteButton = screen.getByText('Delete Pages');
    fireEvent.click(deleteButton);

    await waitFor(() => {
      expect(mockAxios.post).toHaveBeenCalledWith('/delete-pages', expect.any(FormData));
    });
  });

  it('shows loading state during deletion', async () => {
    const mockFile = new File(['test content'], 'test.pdf', { type: 'application/pdf' });

    const mockAxios = vi.mocked(require('axios').default);
    mockAxios.post.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));

    // Mock useDropzone to return a file
    vi.mocked(require('react-dropzone').useDropzone).mockReturnValue({
      getRootProps: () => ({
        onClick: vi.fn(),
      }),
      getInputProps: () => ({}),
      isDragActive: false,
      acceptedFiles: [mockFile],
    });

    render(<DeletePages />);
    
    const pageInput = screen.getByLabelText('Pages to delete (e.g., 1,3-5,7)');
    fireEvent.change(pageInput, { target: { value: '2' } });

    const deleteButton = screen.getByText('Delete Pages');
    fireEvent.click(deleteButton);

    await waitFor(() => {
      expect(screen.getByText('Deleting pages...')).toBeInTheDocument();
    });
  });

  it('handles deletion error', async () => {
    const mockFile = new File(['test content'], 'test.pdf', { type: 'application/pdf' });

    const mockAxios = vi.mocked(require('axios').default);
    mockAxios.post.mockRejectedValue(new Error('Deletion failed'));

    // Mock useDropzone to return a file
    vi.mocked(require('react-dropzone').useDropzone).mockReturnValue({
      getRootProps: () => ({
        onClick: vi.fn(),
      }),
      getInputProps: () => ({}),
      isDragActive: false,
      acceptedFiles: [mockFile],
    });

    render(<DeletePages />);
    
    const pageInput = screen.getByLabelText('Pages to delete (e.g., 1,3-5,7)');
    fireEvent.change(pageInput, { target: { value: '2' } });

    const deleteButton = screen.getByText('Delete Pages');
    fireEvent.click(deleteButton);

    await waitFor(() => {
      expect(screen.getByText('Error deleting pages')).toBeInTheDocument();
    });
  });

  it('validates page input format', async () => {
    const mockFile = new File(['test content'], 'test.pdf', { type: 'application/pdf' });

    // Mock useDropzone to return a file
    vi.mocked(require('react-dropzone').useDropzone).mockReturnValue({
      getRootProps: () => ({
        onClick: vi.fn(),
      }),
      getInputProps: () => ({}),
      isDragActive: false,
      acceptedFiles: [mockFile],
    });

    render(<DeletePages />);
    
    const pageInput = screen.getByLabelText('Pages to delete (e.g., 1,3-5,7)');
    
    // Test valid formats
    fireEvent.change(pageInput, { target: { value: '1,2,3' } });
    expect(pageInput).toHaveValue('1,2,3');
    
    fireEvent.change(pageInput, { target: { value: '1-5' } });
    expect(pageInput).toHaveValue('1-5');
    
    fireEvent.change(pageInput, { target: { value: '1,3-5,7' } });
    expect(pageInput).toHaveValue('1,3-5,7');
  });

  it('shows file name when file is selected', async () => {
    const mockFile = new File(['test content'], 'test.pdf', { type: 'application/pdf' });

    // Mock useDropzone to return a file
    vi.mocked(require('react-dropzone').useDropzone).mockReturnValue({
      getRootProps: () => ({
        onClick: vi.fn(),
      }),
      getInputProps: () => ({}),
      isDragActive: false,
      acceptedFiles: [mockFile],
    });

    render(<DeletePages />);
    
    await waitFor(() => {
      expect(screen.getByText('test.pdf')).toBeInTheDocument();
    });
  });

  it('handles drag active state', () => {
    // Mock useDropzone to show drag active state
    vi.mocked(require('react-dropzone').useDropzone).mockReturnValue({
      getRootProps: () => ({
        onClick: vi.fn(),
      }),
      getInputProps: () => ({}),
      isDragActive: true,
      acceptedFiles: [],
    });

    render(<DeletePages />);
    
    expect(screen.getByText('Drop the file here...')).toBeInTheDocument();
  });

  it('requires page input before allowing deletion', async () => {
    const mockFile = new File(['test content'], 'test.pdf', { type: 'application/pdf' });

    // Mock useDropzone to return a file
    vi.mocked(require('react-dropzone').useDropzone).mockReturnValue({
      getRootProps: () => ({
        onClick: vi.fn(),
      }),
      getInputProps: () => ({}),
      isDragActive: false,
      acceptedFiles: [mockFile],
    });

    render(<DeletePages />);
    
    const deleteButton = screen.getByText('Delete Pages');
    fireEvent.click(deleteButton);

    // Should not make API call without page input
    await waitFor(() => {
      expect(screen.getByText('Please enter pages to delete')).toBeInTheDocument();
    });
  });
}); 