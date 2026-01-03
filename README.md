# Home Price Prediction Agent

A simple LangChain agent chatbot that predicts future home prices using a linear regression model.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Run

```bash
python main.py
```

## Example Usage

```
You: What will home prices be in 5 years?
Assistant: The predicted average home price in 5 years from now is $375,XXX.XX
```

## Project Structure

- `model.py` - Linear regression model with fake housing data
- `agent.py` - LangChain agent with prediction tool
- `main.py` - Chat interface
