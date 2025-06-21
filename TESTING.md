# Testing Guide

This document provides comprehensive information about the test suites for the PDF Tool project.

## Overview

The PDF Tool project includes comprehensive test suites for all three components:

- **Backend (FastAPI)**: Unit tests for API endpoints and PDF processing
- **Frontend (React)**: Component tests using React Testing Library and Vitest
- **CLI (Python)**: Unit tests for command-line functionality

## Test Structure

```
pdftool/
├── backend/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   └── test_main.py
│   ├── requirements-test.txt
│   └── run_tests.py
├── frontend/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── setup.ts
│   │   └── components/
│   │       ├── __init__.py
│   │       ├── MergePDF.test.tsx
│   │       └── DeletePages.test.tsx
│   ├── vitest.config.ts
│   └── package.json (updated with test dependencies)
├── cli/
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_pdf_tool.py
│   ├── requirements-test.txt
│   └── run_tests.py
└── TESTING.md
```

## Backend Tests

### Setup

```bash
cd backend
pip install -r requirements-test.txt
```

### Running Tests

```bash
# Run all tests
python run_tests.py

# Or use pytest directly
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Test Coverage

The backend tests cover:

- **API Endpoints**:
  - `/merge` - PDF merging functionality
  - `/delete-pages` - Page deletion functionality
  - `/page-count/{filename}` - Page count retrieval

- **Error Handling**:
  - Invalid file types
  - Missing parameters
  - File not found scenarios
  - Internal server errors

- **CORS Configuration**:
  - CORS headers presence
  - Localhost origin allowance

- **PDF Processing**:
  - Valid PDF operations
  - Invalid PDF handling
  - Multi-page PDF operations

### Test Files

- `test_main.py`: Main test suite for FastAPI endpoints
- `conftest.py`: Pytest configuration and fixtures

## Frontend Tests

### Setup

```bash
cd frontend
npm install
```

### Running Tests

```bash
# Run tests in watch mode
npm test

# Run tests once
npm run test:run

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

### Test Coverage

The frontend tests cover:

- **Component Rendering**:
  - MergePDF component
  - DeletePages component

- **User Interactions**:
  - File upload via drag & drop
  - Button clicks
  - Form input validation

- **API Integration**:
  - Successful API calls
  - Error handling
  - Loading states

- **State Management**:
  - Component state changes
  - File selection
  - Form validation

### Test Files

- `MergePDF.test.tsx`: Tests for PDF merging component
- `DeletePages.test.tsx`: Tests for page deletion component
- `setup.ts`: Test environment setup
- `vitest.config.ts`: Vitest configuration

## CLI Tests

### Setup

```bash
cd cli
pip install -r requirements-test.txt
```

### Running Tests

```bash
# Run all tests
python run_tests.py

# Or use pytest directly
pytest tests/ -v
```

### Test Coverage

The CLI tests cover:

- **PDFTool Class**:
  - `merge_pdfs()` method
  - `delete_pages()` method
  - `get_page_count()` method

- **Error Handling**:
  - File not found scenarios
  - Invalid file types
  - Invalid page ranges
  - PDF processing errors

- **Interactive Functions**:
  - `interactive_merge()` function
  - `interactive_delete()` function

- **Input Validation**:
  - File existence checks
  - PDF file type validation
  - Page range format validation

### Test Files

- `test_pdf_tool.py`: Main test suite for CLI functionality

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: |
          cd backend
          pip install -r requirements-test.txt
          pytest tests/ -v

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: |
          cd frontend
          npm install
          npm run test:run

  cli-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: |
          cd cli
          pip install -r requirements-test.txt
          pytest tests/ -v
```

### Cloud Build Integration

Add to your `cloudbuild.yaml`:

```yaml
steps:
  # Backend tests
  - name: 'gcr.io/cloud-builders/docker'
    args: ['run', '--rm', '-v', '/workspace:/app', '-w', '/app/backend', 'python:3.9', 'bash', '-c', 'pip install -r requirements-test.txt && pytest tests/ -v']

  # Frontend tests
  - name: 'gcr.io/cloud-builders/docker'
    args: ['run', '--rm', '-v', '/workspace:/app', '-w', '/app/frontend', 'node:18', 'bash', '-c', 'npm install && npm run test:run']
```

## Test Best Practices

### Writing Tests

1. **Follow AAA Pattern**: Arrange, Act, Assert
2. **Use Descriptive Test Names**: Clear, specific test descriptions
3. **Test Edge Cases**: Include error scenarios and boundary conditions
4. **Mock External Dependencies**: Use mocks for API calls and file operations
5. **Clean Up Resources**: Ensure tests don't leave temporary files

### Test Organization

1. **Group Related Tests**: Use test classes and describe blocks
2. **Use Fixtures**: Share common setup code
3. **Keep Tests Independent**: Each test should run in isolation
4. **Use Meaningful Assertions**: Test specific outcomes, not implementation details

### Coverage Goals

- **Backend**: 90%+ code coverage
- **Frontend**: 80%+ component coverage
- **CLI**: 85%+ function coverage

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure test dependencies are installed
2. **Path Issues**: Check working directory and import paths
3. **Mock Issues**: Verify mock setup and cleanup
4. **Async Tests**: Use proper async/await patterns

### Debugging Tests

```bash
# Backend - verbose output
pytest tests/ -v -s

# Frontend - debug mode
npm run test:run -- --reporter=verbose

# CLI - with print statements
pytest tests/ -v -s --tb=long
```

## Performance Testing

### Load Testing (Optional)

For production deployments, consider adding load tests:

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/page-count/test.pdf

# Using Artillery
artillery quick --count 100 --num 10 http://localhost:8000/page-count/test.pdf
```

## Security Testing

### Security Considerations

1. **File Upload Validation**: Test malicious file uploads
2. **Input Sanitization**: Test SQL injection and XSS attempts
3. **Authentication**: Test unauthorized access (when implemented)
4. **Rate Limiting**: Test API rate limiting (when implemented)

## Contributing to Tests

When adding new features:

1. **Write Tests First**: Follow TDD principles
2. **Update Test Documentation**: Keep this guide current
3. **Maintain Coverage**: Ensure new code is well-tested
4. **Review Test Quality**: Ensure tests are meaningful and maintainable

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Vitest Documentation](https://vitest.dev/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/) 