import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import { Activity, TrendingUp, Target } from 'lucide-react';
import './ModelInfo.css';

function ModelInfo({ modelInfo, predictions }) {
  const metricsData = modelInfo?.metadata?.metrics ? [
    { name: 'R² Score', value: modelInfo.metadata.metrics.r2 * 100 },
    { name: 'Accuracy', value: (1 - modelInfo.metadata.metrics.mae / 5) * 100 }
  ] : [];

  const predictionTrend = predictions.slice(-10).map((pred, idx) => ({
    index: idx + 1,
    price: pred.price / 1000
  }));

  return (
    <div className="model-info">
      <div className="info-grid">
        <div className="card">
          <div className="card-header">
            <Activity size={24} />
            <h3>Model Information</h3>
          </div>
          
          {modelInfo?.model_loaded ? (
            <div className="info-content">
              <div className="info-item">
                <span className="info-label">Model Type:</span>
                <span className="info-value">
                  {modelInfo.metadata?.model_type || 'Random Forest'}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">Training Samples:</span>
                <span className="info-value">
                  {modelInfo.metadata?.training_samples?.toLocaleString() || 'N/A'}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">Features:</span>
                <span className="info-value">{modelInfo.feature_names?.length || 0}</span>
              </div>
              
              <div className="features-list">
                <h4>Feature Names:</h4>
                <div className="features-tags">
                  {modelInfo.feature_names?.map((feature, idx) => (
                    <span key={idx} className="feature-tag">{feature}</span>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="no-model">
              <p>No model loaded. Please train a model first.</p>
            </div>
          )}
        </div>

        {modelInfo?.metadata?.metrics && (
          <div className="card">
            <div className="card-header">
              <Target size={24} />
              <h3>Model Performance</h3>
            </div>
            
            <div className="metrics-grid">
              <div className="metric-card">
                <div className="metric-label">R² Score</div>
                <div className="metric-value">
                  {modelInfo.metadata.metrics.r2.toFixed(4)}
                </div>
                <div className="metric-description">Model accuracy</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">RMSE</div>
                <div className="metric-value">
                  ${(modelInfo.metadata.metrics.rmse * 100000).toLocaleString('en-US', { maximumFractionDigits: 0 })}
                </div>
                <div className="metric-description">Root mean squared error</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">MAE</div>
                <div className="metric-value">
                  ${(modelInfo.metadata.metrics.mae * 100000).toLocaleString('en-US', { maximumFractionDigits: 0 })}
                </div>
                <div className="metric-description">Mean absolute error</div>
              </div>
            </div>

            {metricsData.length > 0 && (
              <div className="chart-container">
                <h4>Performance Metrics</h4>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={metricsData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#667eea" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        )}

        {predictionTrend.length > 0 && (
          <div className="card">
            <div className="card-header">
              <TrendingUp size={24} />
              <h3>Prediction Trend</h3>
            </div>
            
            <div className="chart-container">
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={predictionTrend}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="index" />
                  <YAxis />
                  <Tooltip 
                    formatter={(value) => `$${(value * 1000).toLocaleString()}k`}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="price" 
                    stroke="#667eea" 
                    strokeWidth={2}
                    dot={{ fill: '#667eea' }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ModelInfo;
