# 🏠 California Housing Dashboard Agent

An AI-powered real estate analysis platform that combines machine learning, LangChain agents, and a modern React dashboard for predicting California housing prices.

## 🌟 Features

- **ML Model Training**: Train models using the California housing dataset with preprocessing pipeline
- **Dynamic Retraining**: Upload custom CSV datasets to retrain the model with combined data
- **LangChain Agent**: Conversational AI agent for natural language price predictions
- **React Dashboard**: Modern, responsive web interface with:
  - Interactive chatbot interface
  - File upload for custom datasets
  - Real-time price predictions
  - Model performance analytics
  - Visualization charts

## 📁 Project Structure

```
dashboard Agent/
├── frontend/              # React dashboard
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── App.js        # Main app
│   │   └── index.js      # Entry point
│   └── package.json
├── backend/              # FastAPI server
│   └── main.py          # API endpoints
├── ml/                   # ML training & preprocessing
│   ├── train_model.ipynb # Jupyter notebook
│   ├── preprocessing.py  # Data preprocessing
│   └── model_trainer.py  # Model training logic
├── agent/                # LangChain agent
│   ├── agent.py         # Agent definition
│   └── chat.py          # CLI chat interface
├── data/                 # Datasets
│   ├── california_housing.csv
│   └── uploads/         # User uploaded files
├── models/               # Trained models
│   ├── housing_model.pkl
│   ├── scaler.pkl
│   └── metadata.pkl
└── requirements.txt
```

## 🚀 Setup Instructions

### 1. Install Python Dependencies

```bash
cd "dashboard Agent"
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
pip install jupyter  # For notebook
```

### 2. Train the Initial Model

Run the Jupyter notebook to train the model with California housing data:

```bash
jupyter notebook ml/train_model.ipynb
```

Execute all cells to:
- Load California housing dataset
- Preprocess data
- Train Random Forest model
- Save model artifacts

Alternatively, you can train via the API (after starting the backend).

### 3. Configure OpenAI API Key

Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Start the Backend Server

```bash
python backend/main.py
```

The API will be available at `http://localhost:8000`

**API Endpoints:**
- `GET /health` - Health check
- `POST /predict` - Single prediction
- `POST /predict/bulk` - Bulk predictions
- `POST /train` - Train base model
- `POST /retrain` - Retrain with uploaded data
- `GET /model/info` - Model information

### 5. Start the React Frontend

In a new terminal:

```bash
cd frontend
npm install
npm start
```

The dashboard will open at `http://localhost:3000`

### 6. (Optional) Use CLI Agent

For command-line interaction:

```bash
python agent/chat.py
```

## 📊 Using the Dashboard

### Dashboard Tab
- Enter housing features manually
- Get instant price predictions
- View recent predictions

### Chat Agent Tab
- Natural language conversations
- Ask about housing prices
- Get model information

### Upload Data Tab
- Train base model with California dataset
- Upload custom CSV files to retrain
- View training metrics

### Analytics Tab
- Model performance metrics
- Feature information
- Prediction trends visualization

## 📝 Custom Dataset Format

To upload your own data for retraining, your CSV must include:

**Required columns:**
- `MedInc` - Median income (in tens of thousands)
- `HouseAge` - Median house age
- `AveRooms` - Average rooms per household
- `AveBedrms` - Average bedrooms per household
- `Population` - Block group population
- `AveOccup` - Average occupancy
- `Latitude` - Latitude coordinate
- `Longitude` - Longitude coordinate
- `target` - Housing price (in hundreds of thousands)

Example CSV:
```csv
MedInc,HouseAge,AveRooms,AveBedrms,Population,AveOccup,Latitude,Longitude,target
3.5,25.0,5.5,1.2,1200,3.2,34.05,-118.25,2.5
```

## 🔧 Architecture

### Backend (FastAPI)
- RESTful API for predictions
- Model training and retraining endpoints
- File upload handling
- Dynamic model loading

### ML Pipeline
- Data preprocessing with StandardScaler
- Random Forest Regressor
- Model persistence with joblib
- Metrics tracking (R², RMSE, MAE)

### Frontend (React)
- Modern UI with gradient design
- Real-time updates
- Responsive layout
- Chart visualizations (Recharts)

### Agent (LangChain)
- OpenAI GPT-3.5-turbo
- Custom tools for predictions
- Conversational interface
- API integration

## 🎯 Key Features Explained

### Dynamic Model Training
When you upload a CSV file:
1. Your data is validated
2. Combined with California housing dataset
3. Model is retrained on merged data
4. New model replaces the old one
5. All predictions use the updated model

### Preprocessing Pipeline
- Handles missing values (median imputation)
- Feature scaling (StandardScaler)
- Consistent feature ordering
- Automatic feature alignment

### Agent Integration
The LangChain agent:
- Calls FastAPI endpoints
- Provides natural language interface
- Handles multiple features
- Explains predictions

## 🛠️ Technologies Used

- **Backend**: FastAPI, scikit-learn, pandas, numpy
- **Frontend**: React, Recharts, Lucide icons
- **ML**: Random Forest, StandardScaler
- **Agent**: LangChain, OpenAI GPT-3.5
- **Data**: California Housing Dataset

## 📈 Model Performance

The base model trained on California housing data achieves:
- **R² Score**: ~0.80 (80% variance explained)
- **RMSE**: ~$50,000-70,000
- **MAE**: ~$40,000-50,000

Performance varies based on the dataset and retraining.

## 🔒 Security Notes

- Never commit `.env` file with API keys
- Use environment variables for sensitive data
- Validate uploaded CSV files
- Implement rate limiting for production

## 🤝 Contributing

This is a demo project showcasing:
- ML model training and deployment
- FastAPI backend development
- React frontend with modern UI
- LangChain agent integration
- Full-stack ML application

## 📄 License

MIT License - Feel free to use for learning and development.

## 🐛 Troubleshooting

**Model not loading:**
- Run the Jupyter notebook first
- Or use the "Train Base Model" button in the Upload tab

**Backend connection errors:**
- Ensure backend is running on port 8000
- Check CORS settings if accessing from different origin

**Agent not responding:**
- Verify OPENAI_API_KEY in .env file
- Check backend is running
- Ensure model is trained

**Frontend not starting:**
- Run `npm install` in frontend directory
- Check Node.js version (14+ recommended)

## 📞 Support

For issues or questions, check:
1. Backend logs for API errors
2. Browser console for frontend errors
3. Model artifacts exist in `models/` directory
4. All dependencies are installed

---

Built with ❤️ using Python, React, and AI
