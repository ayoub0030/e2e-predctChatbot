# 🚀 Quick Start Guide

Get the California Housing Dashboard Agent running in 5 minutes!

## Step 1: Install Dependencies (2 min)

```bash
cd "dashboard Agent"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install jupyter
```

## Step 2: Train Model (1 min)

Open and run the notebook:
```bash
jupyter notebook ml/train_model.ipynb
```

Click "Run All" or execute each cell. This will:
- Download California housing data
- Train the model
- Save to `models/` directory

## Step 3: Configure API Key (30 sec)

Create `.env` file:
```bash
OPENAI_API_KEY=sk-your-key-here
```

## Step 4: Start Backend (30 sec)

```bash
python backend/main.py
```

Leave this running. You should see:
```
Model loaded successfully
Uvicorn running on http://0.0.0.0:8000
```

## Step 5: Start Frontend (1 min)

Open a NEW terminal:
```bash
cd frontend
npm install
npm start
```

Browser opens automatically at `http://localhost:3000`

## ✅ You're Ready!

Try these:
1. **Dashboard Tab**: Enter features and predict prices
2. **Chat Agent Tab**: Ask "What will a house cost in LA?"
3. **Upload Data Tab**: Upload your own CSV to retrain
4. **Analytics Tab**: View model performance

## 🎯 Test Prediction

In Dashboard tab, use these default values:
- Median Income: 3.0
- House Age: 20
- Avg Rooms: 5
- Avg Bedrooms: 1
- Population: 1000
- Avg Occupancy: 3
- Latitude: 34.0
- Longitude: -118.0

Click "Predict Price" → Should see ~$300,000-400,000

## 🔧 Troubleshooting

**"Model not loaded"**
→ Run the Jupyter notebook first

**"Connection refused"**
→ Make sure backend is running on port 8000

**Agent not working**
→ Check OPENAI_API_KEY in .env file

## 📚 Next Steps

- Upload custom CSV data to retrain
- Chat with the agent about different areas
- View analytics and model performance
- Modify features in the code

Enjoy! 🎉
