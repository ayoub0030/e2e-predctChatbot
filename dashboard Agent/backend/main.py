from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
import pandas as pd
import sys
import os
from typing import List, Dict, Any, Literal, Optional

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ml.preprocessing import preprocess_data, load_model_artifacts, save_model_artifacts
from ml.model_trainer import train_model, retrain_with_user_data
from agent.agent import create_agent

app = FastAPI(title="Housing Price Prediction API")

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
scaler = None
feature_names = None
metadata = None
agent_executor = None

@app.on_event("startup")
async def startup_event():
    """Load the model on startup."""
    global model, scaler, feature_names, metadata, agent_executor
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            agent_executor = create_agent(api_key)
            print("LangChain agent initialized")
        except Exception as agent_error:
            agent_executor = None
            print(f"Warning: Failed to initialize agent - {agent_error}")
    else:
        print("Warning: OPENAI_API_KEY not set. Agent chat will be unavailable.")

    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    model, scaler, feature_names, metadata = load_model_artifacts(models_dir)
    if model is None:
        print("Warning: No trained model found. Please train a model first.")
    else:
        print("Model loaded successfully")


class PredictionRequest(BaseModel):
    features: Dict[str, float]


class PredictionResponse(BaseModel):
    predicted_price: float
    features_used: Dict[str, float]


class BulkPredictionRequest(BaseModel):
    data: List[Dict[str, float]]


class TrainingResponse(BaseModel):
    message: str
    metrics: Dict[str, Any]
    feature_names: List[str]


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ToolOutput(BaseModel):
    tool: str
    tool_input: Any
    output: str


class ChatResponse(BaseModel):
    reply: str
    tool_outputs: Optional[List[ToolOutput]] = None


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "features": feature_names if feature_names else []
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Predict housing price for given features."""
    global model, scaler, feature_names
    
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train a model first.")
    
    try:
        df = pd.DataFrame([request.features])
        
        for feature in feature_names:
            if feature not in df.columns:
                df[feature] = 0.0
        
        df = df[feature_names]
        
        X_scaled, _, _ = preprocess_data(df, scaler=scaler, fit_scaler=False)
        
        prediction = model.predict(X_scaled)[0]
        
        return PredictionResponse(
            predicted_price=float(prediction * 100000),
            features_used=request.features
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict/bulk")
async def predict_bulk(request: BulkPredictionRequest):
    """Predict housing prices for multiple inputs."""
    global model, scaler, feature_names
    
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train a model first.")
    
    try:
        df = pd.DataFrame(request.data)
        
        for feature in feature_names:
            if feature not in df.columns:
                df[feature] = 0.0
        
        df = df[feature_names]
        
        X_scaled, _, _ = preprocess_data(df, scaler=scaler, fit_scaler=False)
        
        predictions = model.predict(X_scaled)
        
        return {
            "predictions": [float(p * 100000) for p in predictions],
            "count": len(predictions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk prediction error: {str(e)}")


@app.post("/train", response_model=TrainingResponse)
async def train_new_model():
    """Train a new model using the California housing dataset."""
    global model, scaler, feature_names, metadata
    
    try:
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'california_housing.csv')
        
        if not os.path.exists(data_path):
            raise HTTPException(status_code=404, detail="California housing dataset not found. Please run the notebook first.")
        
        df = pd.read_csv(data_path)
        
        new_model, new_scaler, metrics, new_feature_names = train_model(df)
        
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        new_metadata = {
            'model_type': 'RandomForestRegressor',
            'features': new_feature_names,
            'metrics': metrics,
            'training_samples': metrics['training_samples']
        }
        save_model_artifacts(new_model, new_scaler, new_feature_names, new_metadata, models_dir)
        
        model = new_model
        scaler = new_scaler
        feature_names = new_feature_names
        metadata = new_metadata
        
        return TrainingResponse(
            message="Model trained successfully",
            metrics=metrics,
            feature_names=new_feature_names
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")


@app.post("/retrain", response_model=TrainingResponse)
async def retrain_model(file: UploadFile = File(...)):
    """Retrain model with user-uploaded CSV data combined with California dataset."""
    global model, scaler, feature_names, metadata
    
    try:
        contents = await file.read()
        
        uploads_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        upload_path = os.path.join(uploads_dir, file.filename)
        with open(upload_path, 'wb') as f:
            f.write(contents)
        
        user_df = pd.read_csv(upload_path)
        
        if 'target' not in user_df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'target' column")
        
        base_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'california_housing.csv')
        new_model, new_scaler, metrics, new_feature_names = retrain_with_user_data(user_df, base_data_path)
        
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        new_metadata = {
            'model_type': 'RandomForestRegressor',
            'features': new_feature_names,
            'metrics': metrics,
            'training_samples': metrics['training_samples'],
            'user_data_file': file.filename
        }
        save_model_artifacts(new_model, new_scaler, new_feature_names, new_metadata, models_dir)
        
        model = new_model
        scaler = new_scaler
        feature_names = new_feature_names
        metadata = new_metadata
        
        return TrainingResponse(
            message=f"Model retrained successfully with {file.filename}",
            metrics=metrics,
            feature_names=new_feature_names
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining error: {str(e)}")


@app.get("/model/info")
async def get_model_info():
    """Get information about the current model."""
    if model is None:
        raise HTTPException(status_code=503, detail="No model loaded")
    
    return {
        "model_loaded": True,
        "feature_names": feature_names,
        "metadata": metadata
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint that routes messages through the LangChain agent."""
    global agent_executor

    if agent_executor is None:
        raise HTTPException(status_code=503, detail="Agent not initialized. Set OPENAI_API_KEY and restart the server.")

    if not request.messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    if request.messages[-1].role != "user":
        raise HTTPException(status_code=400, detail="Last message must come from the user")

    chat_history = []
    for message in request.messages[:-1]:
        if message.role == "user":
            chat_history.append(HumanMessage(content=message.content))
        else:
            chat_history.append(AIMessage(content=message.content))

    user_input = request.messages[-1].content

    try:
        result = await run_in_threadpool(
            agent_executor.invoke,
            {"input": user_input, "chat_history": chat_history}
        )
        reply = result.get("output", "I'm not sure how to respond to that.")

        tool_outputs = []
        for step in result.get("intermediate_steps", []):
            if not step or len(step) != 2:
                continue
            action, observation = step
            tool_outputs.append(
                ToolOutput(
                    tool=getattr(action, "tool", "unknown"),
                    tool_input=getattr(action, "tool_input", None),
                    output=str(observation)
                )
            )

        return ChatResponse(reply=reply, tool_outputs=tool_outputs or None)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Agent error: {exc}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
