import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { datasetAPI, KPIResponse, TimeSeriesPoint, CategoryPoint } from '../services/api';
import '../styles/Dashboard.css';

interface ColumnMapping {
  dateCol: string;
  categoryCol: string;
  valueCol: string;
}

interface DatasetState {
  id: number | null;
  columns: string[];
  preview: Record<string, unknown>[];
  isProcessed: boolean;
}

export const Dashboard: React.FC = () => {
  // State
  const [dataset, setDataset] = useState<DatasetState>({
    id: null,
    columns: [],
    preview: [],
    isProcessed: false,
  });

  const [columnMapping, setColumnMapping] = useState<ColumnMapping>({
    dateCol: '',
    categoryCol: '',
    valueCol: '',
  });

  const [kpis, setKpis] = useState<KPIResponse | null>(null);
  const [timeSeries, setTimeSeries] = useState<TimeSeriesPoint[]>([]);
  const [categories, setCategories] = useState<CategoryPoint[]>([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'upload' | 'mapping' | 'dashboard'>('upload');

  // Colors for charts
  const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1', '#d084d0'];

  // ============================================================================
  // FILE UPLOAD
  // ============================================================================

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      setError('Please select a CSV file');
      return;
    }

    setLoading(true);
    setError(null);

    const response = await datasetAPI.uploadDataset(file);

    if (response.error) {
      setError(response.error);
      setLoading(false);
      return;
    }

    if (response.data) {
      setDataset({
        id: response.data.dataset_id,
        columns: response.data.columns,
        preview: response.data.preview,
        isProcessed: false,
      });

      // Auto-select columns if they match common names
      const mapping: ColumnMapping = {
        dateCol: response.data.columns.find(
          (col) => col.toLowerCase().includes('date') || col.toLowerCase().includes('data')
        ) || '',
        categoryCol: response.data.columns.find(
          (col) => col.toLowerCase().includes('category') || col.toLowerCase().includes('categoria')
        ) || '',
        valueCol: response.data.columns.find(
          (col) => col.toLowerCase().includes('value') || col.toLowerCase().includes('valor')
        ) || '',
      };

      setColumnMapping(mapping);
      setSuccess('CSV uploaded successfully!');
      setActiveTab('mapping');
    }

    setLoading(false);
  };

  // ============================================================================
  // PROCESS DATASET
  // ============================================================================

  const handleProcessDataset = async () => {
    if (!dataset.id || !columnMapping.dateCol || !columnMapping.categoryCol || !columnMapping.valueCol) {
      setError('Please select all required columns');
      return;
    }

    setLoading(true);
    setError(null);

    const response = await datasetAPI.processDataset(
      dataset.id,
      columnMapping.dateCol,
      columnMapping.categoryCol,
      columnMapping.valueCol
    );

    if (response.error) {
      setError(response.error);
      setLoading(false);
      return;
    }

    if (response.data) {
      setDataset((prev) => ({ ...prev, isProcessed: true }));
      setSuccess(
        `Dataset processed! ${response.data.cleaned_rows} rows kept, ${response.data.dropped_rows} rows removed.`
      );
      setActiveTab('dashboard');
      await loadDashboardData();
    }

    setLoading(false);
  };

  // ============================================================================
  // LOAD DASHBOARD DATA
  // ============================================================================

  const loadDashboardData = async () => {
    if (!dataset.id) return;

    setLoading(true);
    setError(null);

    try {
      // Load KPIs
      const kpiResponse = await datasetAPI.getKPIs(dataset.id);
      if (kpiResponse.data) {
        setKpis(kpiResponse.data);
      }

      // Load Time Series
      const timeSeriesResponse = await datasetAPI.getTimeSeries(dataset.id);
      if (timeSeriesResponse.data) {
        setTimeSeries(timeSeriesResponse.data);
      }

      // Load Categories
      const categoriesResponse = await datasetAPI.getCategories(dataset.id);
      if (categoriesResponse.data) {
        setCategories(categoriesResponse.data);
      }
    } catch (err) {
      setError('Failed to load dashboard data');
    }

    setLoading(false);
  };

  // Load dashboard data when dataset is processed
  useEffect(() => {
    if (dataset.isProcessed && dataset.id) {
      loadDashboardData();
    }
  }, [dataset.isProcessed, dataset.id]);

  // ============================================================================
  // RENDER
  // ============================================================================

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>📊 Data Analytics Dashboard</h1>
        <p>Upload, process, and analyze your CSV data</p>
      </header>

      {/* Alerts */}
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      {/* Tabs */}
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          📁 Upload
        </button>
        <button
          className={`tab ${activeTab === 'mapping' ? 'active' : ''}`}
          onClick={() => setActiveTab('mapping')}
          disabled={!dataset.id}
        >
          🔗 Column Mapping
        </button>
        <button
          className={`tab ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
          disabled={!dataset.isProcessed}
        >
          📊 Dashboard
        </button>
      </div>

      {/* Content */}
      <div className="tab-content">
        {/* Upload Tab */}
        {activeTab === 'upload' && (
          <div className="upload-section">
            <div className="upload-box">
              <input
                type="file"
                accept=".csv"
                onChange={handleFileUpload}
                disabled={loading}
                id="csv-input"
              />
              <label htmlFor="csv-input" className="upload-label">
                <span className="upload-icon">📤</span>
                <span className="upload-text">
                  {loading ? 'Uploading...' : 'Click to upload CSV or drag and drop'}
                </span>
              </label>
            </div>

            {dataset.preview.length > 0 && (
              <div className="preview-section">
                <h3>Preview</h3>
                <div className="table-container">
                  <table className="preview-table">
                    <thead>
                      <tr>
                        {dataset.columns.map((col) => (
                          <th key={col}>{col}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {dataset.preview.map((row, idx) => (
                        <tr key={idx}>
                          {dataset.columns.map((col) => (
                            <td key={`${idx}-${col}`}>{String(row[col] || '')}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Column Mapping Tab */}
        {activeTab === 'mapping' && (
          <div className="mapping-section">
            <h2>Select Columns for Analysis</h2>
            <p className="mapping-description">
              Choose which columns represent Date, Category, and Value for your analysis.
            </p>

            <div className="mapping-grid">
              <div className="mapping-item">
                <label>📅 Date Column</label>
                <select
                  value={columnMapping.dateCol}
                  onChange={(e) =>
                    setColumnMapping({ ...columnMapping, dateCol: e.target.value })
                  }
                >
                  <option value="">Select date column</option>
                  {dataset.columns.map((col) => (
                    <option key={col} value={col}>
                      {col}
                    </option>
                  ))}
                </select>
              </div>

              <div className="mapping-item">
                <label>🏷️ Category Column</label>
                <select
                  value={columnMapping.categoryCol}
                  onChange={(e) =>
                    setColumnMapping({ ...columnMapping, categoryCol: e.target.value })
                  }
                >
                  <option value="">Select category column</option>
                  {dataset.columns.map((col) => (
                    <option key={col} value={col}>
                      {col}
                    </option>
                  ))}
                </select>
              </div>

              <div className="mapping-item">
                <label>💰 Value Column</label>
                <select
                  value={columnMapping.valueCol}
                  onChange={(e) =>
                    setColumnMapping({ ...columnMapping, valueCol: e.target.value })
                  }
                >
                  <option value="">Select value column</option>
                  {dataset.columns.map((col) => (
                    <option key={col} value={col}>
                      {col}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <button
              className="btn btn-primary"
              onClick={handleProcessDataset}
              disabled={loading || !columnMapping.dateCol || !columnMapping.categoryCol || !columnMapping.valueCol}
            >
              {loading ? 'Processing...' : 'Process Dataset'}
            </button>
          </div>
        )}

        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && (
          <div className="dashboard-section">
            {/* KPIs */}
            {kpis && (
              <div className="kpis-grid">
                <div className="kpi-card">
                  <div className="kpi-icon">💵</div>
                  <div className="kpi-content">
                    <div className="kpi-label">Total Sum</div>
                    <div className="kpi-value">${kpis.total_sum.toFixed(2)}</div>
                  </div>
                </div>

                <div className="kpi-card">
                  <div className="kpi-icon">📊</div>
                  <div className="kpi-content">
                    <div className="kpi-label">Average</div>
                    <div className="kpi-value">${kpis.average.toFixed(2)}</div>
                  </div>
                </div>

                <div className="kpi-card">
                  <div className="kpi-icon">📈</div>
                  <div className="kpi-content">
                    <div className="kpi-label">Row Count</div>
                    <div className="kpi-value">{kpis.row_count}</div>
                  </div>
                </div>
              </div>
            )}

            {/* Charts */}
            <div className="charts-grid">
              {/* Time Series Chart */}
              {timeSeries.length > 0 && (
                <div className="chart-container">
                  <h3>📈 Time Series</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={timeSeries}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line
                        type="monotone"
                        dataKey="value"
                        stroke="#8884d8"
                        dot={false}
                        name="Value"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              )}

              {/* Category Chart */}
              {categories.length > 0 && (
                <div className="chart-container">
                  <h3>🏷️ By Category</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={categories}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="category" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="value" fill="#82ca9d" name="Value" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              )}

              {/* Pie Chart */}
              {categories.length > 0 && (
                <div className="chart-container">
                  <h3>🥧 Category Distribution</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={categories}
                        dataKey="value"
                        nameKey="category"
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        label
                      >
                        {categories.map((_, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              )}
            </div>

            {/* Export Button */}
            <div className="export-section">
              <button
                className="btn btn-secondary"
                onClick={() => datasetAPI.exportDataset(dataset.id!)}
              >
                📥 Export as CSV
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
