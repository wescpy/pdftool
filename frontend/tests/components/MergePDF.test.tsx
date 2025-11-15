/**
 * Unit tests for the MergePDF component.
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import MergePDF from '../../src/components/MergePDF';

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

describe('MergePDF Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders merge PDF section', () => {
    render(<MergePDF />);
    
    expect(screen.getByText('Merge PDFs')).toBeInTheDocument();
    expect(screen.getByText('Combine multiple PDF files into one')).toBeInTheDocument();
  });

  it('shows drag and drop area', () => {
    render(<MergePDF />);
    
    expect(screen.getByText('Drag & drop PDF files here, or click to select')).toBeInTheDocument();
  });

  it('shows merge button when files are selected', async () => {
    const mockFiles = [
      new File(['test content'], 'test1.pdf', { type: 'application/pdf' }),
      new File(['test content'], 'test2.pdf', { type: 'application/pdf' }),
    ];

    // Mock useDropzone to return files
    vi.mocked(require('react-dropzone').useDropzone).mockReturnValue({
      getRootProps: () => ({
        onClick: vi.fn(),
      }),
      getInputProps: () => ({}),
      isDragActive: false,
      acceptedFiles: mockFiles,
    });

    render(<MergePDF />);
    
    await waitFor(() => {
      expect(screen.getByText('Merge PDFs')).toBeInTheDocument();
    });
  });

  it('handles merge button click', async () => {
    const mockFiles = [
      new File(['test content'], 'test1.pdf', { type: 'application/pdf' }),
      new File(['test content'], 'test2.pdf', { type: 'application/pdf' }),
    ];

    const mockAxios = vi.mocked(require('axios').default);
    mockAxios.post.mockResolvedValue({
      data: new Blob(['merged pdf content'], { type: 'application/pdf' }),
      headers: { 'content-disposition': 'attachment; filename=merged.pdf' },
    });

    // Mock useDropzone to return files
    vi.mocked(require('react-dropzone').useDropzone).mockReturnValue({
      getRootProps: () => ({
        onClick: vi.fn(),
      }),
      getInputProps: () => ({}),
      isDragActive: false,
      acceptedFiles: mockFiles,
    });

    render(<MergePDF />);
    
    const mergeButton = screen.getByText('Merge PDFs');
    fireEvent.click(mergeButton);

    await waitFor(() => {
      expect(mockAxios.post).toHaveBeenCalledWith('/merge', expect.any(FormData));
    });
  });

  it('shows loading state during merge', async () => {
    const mockFiles = [
      new File(['test content'], 'test1.pdf', { type: 'application/pdf' }),
      new File(['test content'], 'test2.pdf', { type: 'application/pdf' }),
    ];

    const mockAxios = vi.mocked(require('axios').default);
    mockAxios.post.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));

    // Mock useDropzone to return files
    vi.mocked(require('react-dropzone').useDropzone).mockReturnValue({
      getRootProps: () => ({
        onClick: vi.fn(),
      }),
      getInputProps: () => ({}),
      isDragActive: false,
      acceptedFiles: mockFiles,
    });

    render(<MergePDF />);
    
    const mergeButton = screen.getByText('Merge PDFs');
    fireEvent.click(mergeButton);

    await waitFor(() => {
      expect(screen.getByText('Merging...')).toBeInTheDocument();
    });
  });

  it('handles merge error', async () => {
    const mockFiles = [
      new File(['test content'], 'test1.pdf', { type: 'application/pdf' }),
      new File(['test content'], 'test2.pdf', { type: 'application/pdf' }),
    ];

    const mockAxios = vi.mocked(require('axios').default);
    mockAxios.post.mockRejectedValue(new Error('Merge failed'));

    // Mock useDropzone to return files
    vi.mocked(require('react-dropzone').useDropzone).mockReturnValue({
      getRootProps: () => ({
        onClick: vi.fn(),
      }),
      getInputProps: () => ({}),
      isDragActive: false,
      acceptedFiles: mockFiles,
    });

    render(<MergePDF />);
    
    const mergeButton = screen.getByText('Merge PDFs');
    fireEvent.click(mergeButton);

    await waitFor(() => {
      expect(screen.getByText('Error merging PDFs')).toBeInTheDocument();
    });
  });

  it('shows file list when files are selected', async () => {
    const mockFiles = [
      new File(['test content'], 'test1.pdf', { type: 'application/pdf' }),
      new File(['test content'], 'test2.pdf', { type: 'application/pdf' }),
    ];

    // Mock useDropzone to return files
    vi.mocked(require('react-dropzone').useDropzone).mockReturnValue({
      getRootProps: () => ({
        onClick: vi.fn(),
      }),
      getInputProps: () => ({}),
      isDragActive: false,
      acceptedFiles: mockFiles,
    });

    render(<MergePDF />);
    
    await waitFor(() => {
      expect(screen.getByText('test1.pdf')).toBeInTheDocument();
      expect(screen.getByText('test2.pdf')).toBeInTheDocument();
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

    render(<MergePDF />);
    
    expect(screen.getByText('Drop the files here...')).toBeInTheDocument();
  });
}); 