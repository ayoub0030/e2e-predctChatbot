from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import requests


@tool
def predict_future_home_price(years_from_now: int) -> str:
    """Predict the average home price for a given number of years from now.
    Use this tool when the user asks about future home prices.
    
    Args:
        years_from_now: Number of years in the future to predict (e.g., 1, 2, 5, 10)
    
    Returns:
        A string with the predicted home price.
    """
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json={"years_from_now": years_from_now},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        price = data["predicted_price"]
        return f"The predicted average home price in {years_from_now} year(s) from now is ${price:,.2f}"
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the prediction API. Make sure the FastAPI server is running on http://localhost:8000"
    except Exception as e:
        return f"Error calling prediction API: {str(e)}"


def create_agent(api_key: str):
    """Create and return the LangChain agent."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=api_key
    )
    
    tools = [predict_future_home_price]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful real estate assistant that can predict future home prices.
When users ask about future home prices, use the predict_future_home_price tool to get predictions.
Be friendly and explain the predictions in a helpful way.
Note: The predictions are based on a simple linear regression model with simulated data for demo purposes."""),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor
