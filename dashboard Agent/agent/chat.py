import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(__file__))
from agent import create_agent

load_dotenv()

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        return
    
    agent = create_agent(api_key)
    
    print("=" * 60)
    print("California Housing Price Prediction Chatbot")
    print("Ask me about housing prices in California!")
    print("Type 'quit' to exit")
    print("=" * 60)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            response = agent.invoke({"input": user_input})
            print(f"\nAssistant: {response['output']}")
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
