import React, { useState } from 'react';
import { Upload, CheckCircle, AlertCircle, Loader } from 'lucide-react';
import './FileUpload.css';

function FileUpload({ onModelRetrained }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'text/csv') {
      setFile(selectedFile);
      setError(null);
      setResult(null);
    } else {
      setError('Please select a valid CSV file');
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/retrain', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      setResult(data);
      if (onModelRetrained) {
        onModelRetrained();
      }
    } catch (err) {
      setError('Failed to upload and retrain model. Make sure the backend is running and the CSV has a "target" column.');
    } finally {
      setUploading(false);
    }
  };

  const handleTrainBase = async () => {
    setUploading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/train', {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Training failed');
      }

      const data = await response.json();
      setResult(data);
      if (onModelRetrained) {
        onModelRetrained();
      }
    } catch (err) {
      setError('Failed to train model. Make sure the backend is running and the California dataset exists.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-card">
        <div className="upload-header">
          <Upload size={32} />
          <h2>Model Training & Data Upload</h2>
          <p>Train the model with California housing data or upload your own dataset</p>
        </div>

        <div className="upload-section">
          <h3>Train Base Model</h3>
          <p className="section-description">
            Train the model using the California housing dataset
          </p>
          <button 
            onClick={handleTrainBase} 
            disabled={uploading}
            className="train-button"
          >
            {uploading ? <Loader className="spin" size={20} /> : 'Train Base Model'}
          </button>
        </div>

        <div className="divider">
          <span>OR</span>
        </div>

        <div className="upload-section">
          <h3>Upload Custom Dataset</h3>
          <p className="section-description">
            Upload a CSV file with housing data to retrain the model. Your data will be combined with the California dataset.
          </p>
          <p className="requirements">
            <strong>Requirements:</strong> CSV file with columns matching California housing features and a "target" column for prices.
          </p>

          <div className="file-input-wrapper">
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              id="file-input"
              className="file-input"
            />
            <label htmlFor="file-input" className="file-label">
              <Upload size={20} />
              {file ? file.name : 'Choose CSV file'}
            </label>
          </div>

          {file && (
            <button 
              onClick={handleUpload} 
              disabled={uploading}
              className="upload-button"
            >
              {uploading ? (
                <>
                  <Loader className="spin" size={20} />
                  Retraining Model...
                </>
              ) : (
                <>
                  <Upload size={20} />
                  Upload & Retrain Model
                </>
              )}
            </button>
          )}
        </div>

        {error && (
          <div className="alert error">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        {result && (
          <div className="alert success">
            <CheckCircle size={20} />
            <div className="result-content">
              <strong>{result.message}</strong>
              <div className="metrics">
                <p>R² Score: {result.metrics.r2.toFixed(4)}</p>
                <p>RMSE: ${(result.metrics.rmse * 100000).toLocaleString('en-US', { maximumFractionDigits: 2 })}</p>
                <p>Training Samples: {result.metrics.training_samples}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default FileUpload;
