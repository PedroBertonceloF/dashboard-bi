import React, { useEffect, useState } from 'react';
import { useAuth } from '../AuthContext';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export const Dashboard = () => {
  const { token, logout } = useAuth();
  const [user, setUser] = useState<{email: string} | null>(null);
  
  // Upload state
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  
  // Preview state
  const [datasetId, setDatasetId] = useState<number | null>(null);
  const [columns, setColumns] = useState<string[]>([]);
  const [previewData, setPreviewData] = useState<any[]>([]);

  // Mapping state
  const [dateCol, setDateCol] = useState('');
  const [categoryCol, setCategoryCol] = useState('');
  const [valueCol, setValueCol] = useState('');
  const [processing, setProcessing] = useState(false);
  
  // Stats state
  const [stats, setStats] = useState<{original_rows: number, cleaned_rows: number, dropped_rows: number} | null>(null);

  // KPI state
  const [kpis, setKpis] = useState<{total_sum: number, average: number, row_count: number} | null>(null);
  const [loadingKpis, setLoadingKpis] = useState(false);

  // Charts state
  const [timeSeriesData, setTimeSeriesData] = useState<any[] | null>(null);
  const [categoryData, setCategoryData] = useState<any[] | null>(null);
  const [loadingCharts, setLoadingCharts] = useState(false);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await fetch('/api/users/me', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (res.ok) {
          const data = await res.json();
          setUser(data);
        } else {
          logout(); // Invalid token
        }
      } catch (err) {
        console.error('Failed to fetch user', err);
      }
    };
    
    if (token) {
      fetchUser();
    }
  }, [token, logout]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/datasets/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Upload failed');
      }

      setDatasetId(data.dataset_id);
      setColumns(data.columns);
      setPreviewData(data.preview);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  const handleProcess = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!datasetId || !dateCol || !categoryCol || !valueCol) return;

    setProcessing(true);
    setError('');

    try {
      const response = await fetch(`/api/datasets/${datasetId}/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          date_col: dateCol,
          category_col: categoryCol,
          value_col: valueCol
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Processing failed');
      }

      setStats({
        original_rows: data.original_rows,
        cleaned_rows: data.cleaned_rows,
        dropped_rows: data.dropped_rows
      });
    } catch (err: any) {
      setError(err.message);
    } finally {
      setProcessing(false);
    }
  };

  const fetchKpis = async () => {
    if (!datasetId) return;
    setLoadingKpis(true);
    setError('');
    
    try {
      const response = await fetch(`/api/datasets/${datasetId}/kpis`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to fetch KPIs');
      }

      setKpis(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoadingKpis(false);
    }
  };

  const fetchCharts = async () => {
    if (!datasetId) return;
    setLoadingCharts(true);
    setError('');
    
    try {
      const [timeRes, catRes] = await Promise.all([
        fetch(`/api/datasets/${datasetId}/charts/timeseries`, { headers: { 'Authorization': `Bearer ${token}` } }),
        fetch(`/api/datasets/${datasetId}/charts/categories`, { headers: { 'Authorization': `Bearer ${token}` } })
      ]);

      const timeData = await timeRes.json();
      const catData = await catRes.json();

      if (!timeRes.ok) throw new Error(timeData.detail || 'Failed to fetch timeseries');
      if (!catRes.ok) throw new Error(catData.detail || 'Failed to fetch categories');

      setTimeSeriesData(timeData);
      setCategoryData(catData);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoadingCharts(false);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Dashboard Wizard</h2>
        <button onClick={logout}>Logout ({user?.email})</button>
      </div>

      {!datasetId && (
        <div style={{ marginTop: '2rem', border: '1px solid #ccc', padding: '1rem', borderRadius: '8px' }}>
          <h3>Step 1: Upload CSV</h3>
          {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}
          <form onSubmit={handleUpload}>
            <input type="file" accept=".csv" onChange={handleFileChange} required />
            <br /><br />
            <button type="submit" disabled={!file || uploading}>
              {uploading ? 'Uploading...' : 'Upload'}
            </button>
          </form>
        </div>
      )}

      {datasetId && !stats && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Step 2: Column Mapping</h3>
          {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}
          
          <div style={{ marginBottom: '2rem', padding: '1rem', background: '#f9f9f9', borderRadius: '8px' }}>
            <form onSubmit={handleProcess} style={{ display: 'flex', gap: '1rem', alignItems: 'flex-end' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Date Column</label>
                <select value={dateCol} onChange={e => setDateCol(e.target.value)} required>
                  <option value="">-- Select --</option>
                  {columns.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Category Column</label>
                <select value={categoryCol} onChange={e => setCategoryCol(e.target.value)} required>
                  <option value="">-- Select --</option>
                  {columns.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem' }}>Value Column (Numeric)</label>
                <select value={valueCol} onChange={e => setValueCol(e.target.value)} required>
                  <option value="">-- Select --</option>
                  {columns.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <button type="submit" disabled={processing || !dateCol || !categoryCol || !valueCol}>
                {processing ? 'Processing...' : 'Clean Data'}
              </button>
            </form>
          </div>

          <h3>Data Preview</h3>
          <div style={{ overflowX: 'auto', border: '1px solid #ddd', borderRadius: '4px' }}>
            <table border={1} cellPadding={8} style={{ borderCollapse: 'collapse', width: '100%', textAlign: 'left' }}>
              <thead style={{ backgroundColor: '#f5f5f5', color: 'black' }}>
                <tr>
                  {columns.map(col => (
                    <th key={col}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {previewData.map((row, idx) => (
                  <tr key={idx}>
                    {columns.map(col => (
                      <td key={col}>{row[col] !== null ? String(row[col]) : <i>null</i>}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {stats && !kpis && (
        <div style={{ marginTop: '2rem', padding: '1rem', background: '#e6ffe6', borderRadius: '8px', border: '1px solid #b3ffb3' }}>
          <h3>✅ Data Cleaned Successfully</h3>
          <p>We applied the strict data dropping policy to ensure data integrity.</p>
          <ul>
            <li><strong>Original Rows:</strong> {stats.original_rows}</li>
            <li><strong>Valid Rows Kept:</strong> {stats.cleaned_rows}</li>
            <li style={{ color: stats.dropped_rows > 0 ? 'red' : 'inherit' }}>
              <strong>Invalid Rows Dropped:</strong> {stats.dropped_rows}
            </li>
          </ul>
          
          <button style={{ marginTop: '1rem' }} onClick={fetchKpis} disabled={loadingKpis}>
            {loadingKpis ? 'Loading Analytics...' : 'Generate Dashboard KPIs'}
          </button>
        </div>
      )}

      {kpis && (
        <div style={{ marginTop: '2rem' }}>
          <h3>Core KPIs</h3>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <div style={{ flex: 1, padding: '1.5rem', background: '#f0f4f8', borderRadius: '8px', border: '1px solid #d9e2ec', textAlign: 'center' }}>
              <h4 style={{ margin: '0 0 0.5rem 0', color: '#334e68' }}>Total {valueCol}</h4>
              <p style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold', color: '#102a43' }}>
                {kpis.total_sum.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </p>
            </div>
            
            <div style={{ flex: 1, padding: '1.5rem', background: '#f0f4f8', borderRadius: '8px', border: '1px solid #d9e2ec', textAlign: 'center' }}>
              <h4 style={{ margin: '0 0 0.5rem 0', color: '#334e68' }}>Average {valueCol}</h4>
              <p style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold', color: '#102a43' }}>
                {kpis.average.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </p>
            </div>
            
            <div style={{ flex: 1, padding: '1.5rem', background: '#f0f4f8', borderRadius: '8px', border: '1px solid #d9e2ec', textAlign: 'center' }}>
              <h4 style={{ margin: '0 0 0.5rem 0', color: '#334e68' }}>Valid Records</h4>
              <p style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold', color: '#102a43' }}>
                {kpis.row_count}
              </p>
            </div>
          </div>
          
          {!timeSeriesData && (
            <div style={{ marginTop: '2rem', textAlign: 'center' }}>
              <button onClick={fetchCharts} disabled={loadingCharts}>
                {loadingCharts ? 'Loading Charts...' : 'Generate Dashboard Charts'}
              </button>
            </div>
          )}

          {timeSeriesData && categoryData && (
            <div style={{ marginTop: '3rem' }}>
              <h3>Dashboard Visualizations</h3>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
                
                {/* Time Series Chart */}
                <div style={{ height: '400px', width: '100%', background: 'white', padding: '1rem', border: '1px solid #ddd', borderRadius: '8px' }}>
                  <h4 style={{ textAlign: 'center', marginBottom: '1rem', color: '#333' }}>Trend Over Time ({valueCol} by {dateCol})</h4>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={timeSeriesData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} />
                      <XAxis dataKey="date" tick={{ fill: '#666' }} />
                      <YAxis tick={{ fill: '#666' }} />
                      <Tooltip 
                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}
                        formatter={(value: any) => Number(value).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                      />
                      <Legend />
                      <Line type="monotone" dataKey="value" name={valueCol} stroke="#3b82f6" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>

                {/* Category Bar Chart */}
                <div style={{ height: '400px', width: '100%', background: 'white', padding: '1rem', border: '1px solid #ddd', borderRadius: '8px' }}>
                  <h4 style={{ textAlign: 'center', marginBottom: '1rem', color: '#333' }}>Total by Category ({valueCol} by {categoryCol})</h4>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={categoryData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} />
                      <XAxis dataKey="category" tick={{ fill: '#666' }} />
                      <YAxis tick={{ fill: '#666' }} />
                      <Tooltip 
                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px rgba(0,0,0,0.1)' }}
                        formatter={(value: any) => Number(value).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                      />
                      <Legend />
                      <Bar dataKey="value" name={valueCol} fill="#10b981" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>

              </div>

              <div style={{ marginTop: '2rem', textAlign: 'center' }}>
                <button onClick={() => alert("Próximo passo: Issue #6 Interatividade!")}>
                  Continue to Interactive Filters
                </button>
              </div>

            </div>
          )}
        </div>
      )}
    </div>
  );
};
