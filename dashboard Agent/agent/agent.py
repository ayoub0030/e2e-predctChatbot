from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import requests
import json


@tool
def predict_housing_price(
    MedInc: float = 3.0,
    HouseAge: float = 20.0,
    AveRooms: float = 5.0,
    AveBedrms: float = 1.0,
    Population: float = 1000.0,
    AveOccup: float = 3.0,
    Latitude: float = 34.0,
    Longitude: float = -118.0
) -> str:
    """Predict California housing price based on property features.
    
    Args:
        MedInc: Median income in block group (in tens of thousands)
        HouseAge: Median house age in block group
        AveRooms: Average number of rooms per household
        AveBedrms: Average number of bedrooms per household
        Population: Block group population
        AveOccup: Average number of household members
        Latitude: Block group latitude
        Longitude: Block group longitude
    
    Returns:
        Predicted housing price as a formatted string.
    """
    try:
        features = {
            "MedInc": MedInc,
            "HouseAge": HouseAge,
            "AveRooms": AveRooms,
            "AveBedrms": AveBedrms,
            "Population": Population,
            "AveOccup": AveOccup,
            "Latitude": Latitude,
            "Longitude": Longitude
        }
        
        response = requests.post(
            "http://localhost:8000/predict",
            json={"features": features},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        price = data["predicted_price"]
        return f"The predicted housing price is ${price:,.2f} based on the provided features."
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the prediction API. Make sure the FastAPI server is running on http://localhost:8000"
    except Exception as e:
        return f"Error calling prediction API: {str(e)}"


@tool
def get_model_info() -> str:
    """Get information about the current housing price prediction model.
    
    Returns:
        Model information including features and performance metrics.
    """
    try:
        response = requests.get(
            "http://localhost:8000/model/info",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        
        if not data.get("model_loaded"):
            return "No model is currently loaded."
        
        info = f"Model Information:\n"
        info += f"Features: {', '.join(data['feature_names'])}\n"
        
        if data.get('metadata'):
            metadata = data['metadata']
            if 'metrics' in metadata:
                metrics = metadata['metrics']
                info += f"\nPerformance Metrics:\n"
                info += f"  - R² Score: {metrics.get('r2', 'N/A'):.4f}\n"
                info += f"  - RMSE: ${metrics.get('rmse', 0)*100000:,.2f}\n"
                info += f"  - MAE: ${metrics.get('mae', 0)*100000:,.2f}\n"
            info += f"Training Samples: {metadata.get('training_samples', 'N/A')}\n"
        
        return info
    except Exception as e:
        return f"Error getting model info: {str(e)}"


def create_agent(api_key: str):
    """Create and return the LangChain agent for housing price predictions."""
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key=api_key
    )
    
    tools = [predict_housing_price, get_model_info]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful California housing price prediction assistant.

You can predict housing prices based on various features like median income, house age, location, etc.

When users ask about housing prices:
1. Ask for relevant features if not provided (median income, house age, rooms, bedrooms, population, occupancy, latitude, longitude)
2. Use reasonable defaults for California if specific values aren't given
3. Use the predict_housing_price tool to get predictions
4. Explain the prediction in a helpful, conversational way

You can also provide information about the model using the get_model_info tool.

Be friendly and help users understand what factors affect housing prices."""),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor
