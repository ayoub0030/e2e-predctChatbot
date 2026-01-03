import os
from dotenv import load_dotenv
from agent import create_agent

load_dotenv()

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        print("Example: OPENAI_API_KEY=sk-your-key-here")
        return
    
    agent = create_agent(api_key)
    
    print("=" * 50)
    print("Home Price Prediction Chatbot")
    print("Ask me about future home prices!")
    print("Type 'quit' to exit")
    print("=" * 50)
    
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
