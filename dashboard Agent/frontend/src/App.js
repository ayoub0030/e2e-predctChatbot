import React, { useState, useEffect } from 'react';
import './App.css';
import Chatbot from './components/Chatbot';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import ModelInfo from './components/ModelInfo';
import { Home, MessageSquare, Upload, BarChart3 } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [modelInfo, setModelInfo] = useState(null);
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    fetchModelInfo();
  }, []);

  const fetchModelInfo = async () => {
    try {
      const response = await fetch('http://localhost:8000/model/info');
      const data = await response.json();
      setModelInfo(data);
    } catch (error) {
      console.error('Error fetching model info:', error);
    }
  };

  const handlePrediction = (prediction) => {
    setPredictions(prev => [...prev, { ...prediction, timestamp: new Date() }]);
  };

  const handleModelRetrained = () => {
    fetchModelInfo();
  };

  return (
    <div className="App">
      <header className="header">
        <div className="header-content">
          <h1>🏠 California Housing Price Predictor</h1>
          <p>AI-Powered Real Estate Analysis Dashboard</p>
        </div>
      </header>

      <nav className="nav-tabs">
        <button
          className={`tab ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          <Home size={20} />
          <span>Dashboard</span>
        </button>
        <button
          className={`tab ${activeTab === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveTab('chat')}
        >
          <MessageSquare size={20} />
          <span>Chat Agent</span>
        </button>
        <button
          className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          <Upload size={20} />
          <span>Upload Data</span>
        </button>
        <button
          className={`tab ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          <BarChart3 size={20} />
          <span>Analytics</span>
        </button>
      </nav>

      <main className="main-content">
        {activeTab === 'dashboard' && (
          <Dashboard predictions={predictions} modelInfo={modelInfo} />
        )}
        {activeTab === 'chat' && (
          <Chatbot onPrediction={handlePrediction} />
        )}
        {activeTab === 'upload' && (
          <FileUpload onModelRetrained={handleModelRetrained} />
        )}
        {activeTab === 'analytics' && (
          <ModelInfo modelInfo={modelInfo} predictions={predictions} />
        )}
      </main>
    </div>
  );
}

export default App;
