/**
 * API Service - Handles all communication with the backend
 * Uses proxy configured in vite.config.ts to avoid CORS issues
 */

const API_URL = '/api'; // Uses proxy from vite.config.ts

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface UserResponse {
  id: number;
  email: string;
}

export interface DatasetResponse {
  dataset_id: number;
  columns: string[];
  preview: Record<string, unknown>[];
}

export interface ProcessResponse {
  message: string;
  original_rows: number;
  cleaned_rows: number;
  dropped_rows: number;
}

export interface KPIResponse {
  total_sum: number;
  average: number;
  row_count: number;
}

export interface TimeSeriesPoint {
  date: string;
  value: number;
}

export interface CategoryPoint {
  category: string;
  value: number;
}

/**
 * Get authorization token from localStorage
 */
function getAuthToken(): string | null {
  return localStorage.getItem('token');
}

function setAuthToken(token: string): void {
  localStorage.setItem('token', token);
}

function clearAuthToken(): void {
  localStorage.removeItem('token');
}

/**
 * Make API request with error handling
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const token = getAuthToken();
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    // Handle 401 Unauthorized
    if (response.status === 401) {
      clearAuthToken();
      window.location.href = '/login';
      return { status: 401, error: 'Unauthorized' };
    }

    const data = await response.json();

    if (!response.ok) {
      return {
        status: response.status,
        error: data.detail || 'An error occurred',
      };
    }

    return {
      data,
      status: response.status,
    };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Network error';
    console.error('API Error:', errorMessage);
    return {
      status: 0,
      error: errorMessage,
    };
  }
}

/**
 * Upload file with FormData
 */
async function uploadFile<T>(
  endpoint: string,
  file: File
): Promise<ApiResponse<T>> {
  try {
    const token = getAuthToken();
    const formData = new FormData();
    formData.append('file', file);

    const headers: HeadersInit = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers,
      body: formData,
    });

    if (response.status === 401) {
      clearAuthToken();
      window.location.href = '/login';
      return { status: 401, error: 'Unauthorized' };
    }

    const data = await response.json();

    if (!response.ok) {
      return {
        status: response.status,
        error: data.detail || 'Upload failed',
      };
    }

    return {
      data,
      status: response.status,
    };
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Upload failed';
    console.error('Upload Error:', errorMessage);
    return {
      status: 0,
      error: errorMessage,
    };
  }
}

// ============================================================================
// AUTH ENDPOINTS
// ============================================================================

export const authAPI = {
  /**
   * Register a new user
   */
  register: async (email: string, password: string): Promise<ApiResponse<UserResponse>> => {
    return apiRequest<UserResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  },

  /**
   * Login user
   */
  login: async (email: string, password: string): Promise<ApiResponse<AuthResponse>> => {
    const response = await apiRequest<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });

    if (response.data?.access_token) {
      setAuthToken(response.data.access_token);
    }

    return response;
  },

  /**
   * Get current user info
   */
  getCurrentUser: async (): Promise<ApiResponse<UserResponse>> => {
    return apiRequest<UserResponse>('/users/me');
  },

  /**
   * Logout user
   */
  logout: (): void => {
    clearAuthToken();
  },
};

// ============================================================================
// DATASET ENDPOINTS
// ============================================================================

export const datasetAPI = {
  /**
   * Upload CSV file
   */
  uploadDataset: async (file: File): Promise<ApiResponse<DatasetResponse>> => {
    return uploadFile<DatasetResponse>('/datasets/upload', file);
  },

  /**
   * Process and clean dataset
   */
  processDataset: async (
    datasetId: number,
    dateCol: string,
    categoryCol: string,
    valueCol: string
  ): Promise<ApiResponse<ProcessResponse>> => {
    return apiRequest<ProcessResponse>(`/datasets/${datasetId}/process`, {
      method: 'POST',
      body: JSON.stringify({
        date_col: dateCol,
        category_col: categoryCol,
        value_col: valueCol,
      }),
    });
  },

  /**
   * Get KPIs for dataset
   */
  getKPIs: async (
    datasetId: number,
    startDate?: string,
    endDate?: string,
    categories?: string
  ): Promise<ApiResponse<KPIResponse>> => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    if (categories) params.append('categories', categories);

    const query = params.toString();
    const endpoint = `/datasets/${datasetId}/kpis${query ? `?${query}` : ''}`;

    return apiRequest<KPIResponse>(endpoint);
  },

  /**
   * Get time series data
   */
  getTimeSeries: async (
    datasetId: number,
    startDate?: string,
    endDate?: string,
    categories?: string
  ): Promise<ApiResponse<TimeSeriesPoint[]>> => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    if (categories) params.append('categories', categories);

    const query = params.toString();
    const endpoint = `/datasets/${datasetId}/charts/timeseries${query ? `?${query}` : ''}`;

    return apiRequest<TimeSeriesPoint[]>(endpoint);
  },

  /**
   * Get category data
   */
  getCategories: async (
    datasetId: number,
    startDate?: string,
    endDate?: string,
    categories?: string
  ): Promise<ApiResponse<CategoryPoint[]>> => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    if (categories) params.append('categories', categories);

    const query = params.toString();
    const endpoint = `/datasets/${datasetId}/charts/categories${query ? `?${query}` : ''}`;

    return apiRequest<CategoryPoint[]>(endpoint);
  },

  /**
   * Export dataset as CSV
   */
  exportDataset: async (
    datasetId: number,
    startDate?: string,
    endDate?: string,
    categories?: string
  ): Promise<void> => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    if (categories) params.append('categories', categories);

    const query = params.toString();
    const endpoint = `/datasets/${datasetId}/export${query ? `?${query}` : ''}`;

    const token = getAuthToken();
    const headers: HeadersInit = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, { headers });
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `export_${datasetId}.csv`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },
};

export default {
  authAPI,
  datasetAPI,
};
