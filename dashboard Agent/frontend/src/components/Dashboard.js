import React, { useState } from 'react';
import { TrendingUp, DollarSign, Home, MapPin } from 'lucide-react';
import './Dashboard.css';

function Dashboard({ predictions, modelInfo }) {
  const [formData, setFormData] = useState({
    MedInc: 3.0,
    HouseAge: 20.0,
    AveRooms: 5.0,
    AveBedrms: 1.0,
    Population: 1000.0,
    AveOccup: 3.0,
    Latitude: 34.0,
    Longitude: -118.0
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: parseFloat(e.target.value) || 0
    });
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ features: formData })
      });

      const data = await response.json();
      setPrediction(data.predicted_price);
    } catch (error) {
      console.error('Prediction error:', error);
      alert('Failed to get prediction. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-grid">
        <div className="card stats-card">
          <div className="card-header">
            <Home size={24} />
            <h3>Quick Stats</h3>
          </div>
          <div className="stats-grid">
            <div className="stat">
              <div className="stat-label">Model Status</div>
              <div className="stat-value">
                {modelInfo?.model_loaded ? '✓ Active' : '✗ Not Loaded'}
              </div>
            </div>
            <div className="stat">
              <div className="stat-label">Predictions Made</div>
              <div className="stat-value">{predictions.length}</div>
            </div>
            <div className="stat">
              <div className="stat-label">Features</div>
              <div className="stat-value">{modelInfo?.feature_names?.length || 0}</div>
            </div>
          </div>
        </div>

        <div className="card prediction-card">
          <div className="card-header">
            <DollarSign size={24} />
            <h3>Price Prediction</h3>
          </div>
          
          <form onSubmit={handlePredict} className="prediction-form">
            <div className="form-grid">
              <div className="form-group">
                <label>Median Income (10k)</label>
                <input
                  type="number"
                  name="MedInc"
                  value={formData.MedInc}
                  onChange={handleChange}
                  step="0.1"
                />
              </div>
              <div className="form-group">
                <label>House Age (years)</label>
                <input
                  type="number"
                  name="HouseAge"
                  value={formData.HouseAge}
                  onChange={handleChange}
                  step="1"
                />
              </div>
              <div className="form-group">
                <label>Avg Rooms</label>
                <input
                  type="number"
                  name="AveRooms"
                  value={formData.AveRooms}
                  onChange={handleChange}
                  step="0.1"
                />
              </div>
              <div className="form-group">
                <label>Avg Bedrooms</label>
                <input
                  type="number"
                  name="AveBedrms"
                  value={formData.AveBedrms}
                  onChange={handleChange}
                  step="0.1"
                />
              </div>
              <div className="form-group">
                <label>Population</label>
                <input
                  type="number"
                  name="Population"
                  value={formData.Population}
                  onChange={handleChange}
                  step="10"
                />
              </div>
              <div className="form-group">
                <label>Avg Occupancy</label>
                <input
                  type="number"
                  name="AveOccup"
                  value={formData.AveOccup}
                  onChange={handleChange}
                  step="0.1"
                />
              </div>
              <div className="form-group">
                <label>Latitude</label>
                <input
                  type="number"
                  name="Latitude"
                  value={formData.Latitude}
                  onChange={handleChange}
                  step="0.01"
                />
              </div>
              <div className="form-group">
                <label>Longitude</label>
                <input
                  type="number"
                  name="Longitude"
                  value={formData.Longitude}
                  onChange={handleChange}
                  step="0.01"
                />
              </div>
            </div>

            <button type="submit" disabled={loading} className="predict-button">
              {loading ? 'Predicting...' : 'Predict Price'}
            </button>
          </form>

          {prediction !== null && (
            <div className="prediction-result">
              <TrendingUp size={32} />
              <div className="result-content">
                <div className="result-label">Predicted Price</div>
                <div className="result-value">
                  ${prediction.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </div>
              </div>
            </div>
          )}
        </div>

        {predictions.length > 0 && (
          <div className="card recent-predictions">
            <div className="card-header">
              <MapPin size={24} />
              <h3>Recent Predictions</h3>
            </div>
            <div className="predictions-list">
              {predictions.slice(-5).reverse().map((pred, idx) => (
                <div key={idx} className="prediction-item">
                  <div className="prediction-price">
                    ${pred.price?.toLocaleString('en-US', { maximumFractionDigits: 0 })}
                  </div>
                  <div className="prediction-time">
                    {pred.timestamp?.toLocaleTimeString()}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
