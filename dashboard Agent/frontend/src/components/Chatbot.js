import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, AlertTriangle, Wrench } from 'lucide-react';
import './Chatbot.css';

function Chatbot({ onPrediction }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! I can help you predict California housing prices. Ask me about housing prices in different areas!' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const messagesRef = useRef(messages);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    messagesRef.current = messages;
    scrollToBottom();
  }, [messages]);

  const formatToolOutput = (toolOutput) => {
    const { tool, tool_input: toolInput, output } = toolOutput;

    const formattedInput = (() => {
      if (!toolInput) return 'None';
      if (typeof toolInput === 'string') {
        try {
          const parsed = JSON.parse(toolInput);
          return JSON.stringify(parsed, null, 2);
        } catch (e) {
          return toolInput;
        }
      }
      return JSON.stringify(toolInput, null, 2);
    })();

    return {
      tool,
      input: formattedInput,
      output
    };
  };

  const handleToolSideEffects = (toolOutputs) => {
    if (!onPrediction || !Array.isArray(toolOutputs)) return;

    toolOutputs.forEach((toolOutput) => {
      if (toolOutput.tool === 'predict_housing_price') {
        const priceMatch = toolOutput.output?.match(/\$([\d,.,]+)/);
        const price = priceMatch ? parseFloat(priceMatch[1].replace(/,/g, '')) : undefined;
        const features = toolOutput.tool_input && typeof toolOutput.tool_input === 'object'
          ? toolOutput.tool_input
          : undefined;

        onPrediction({ price, features, raw: toolOutput.output });
      }
    });
  };

  const renderMessageContent = (message) => {
    if (message.role === 'tool' && message.toolMeta) {
      const { tool, input, output } = message.toolMeta;
      return (
        <div className="tool-message">
          <div className="tool-name">Tool: {tool}</div>
          <div className="tool-section">
            <strong>Input</strong>
            <pre>{input}</pre>
          </div>
          <div className="tool-section">
            <strong>Output</strong>
            <p>{output}</p>
          </div>
        </div>
      );
    }

    return <span>{message.content}</span>;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);
    setError(null);

    try {
      const conversation = [...messagesRef.current, { role: 'user', content: userMessage }];
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: conversation })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Chat request failed');
      }

      const data = await response.json();
      const assistantMessage = data.reply || "I'm not sure how to respond to that.";

      setMessages(prev => {
        let next = [...prev, { role: 'assistant', content: assistantMessage }];

        if (Array.isArray(data.tool_outputs) && data.tool_outputs.length > 0) {
          data.tool_outputs.forEach((toolOutput) => {
            const toolMeta = formatToolOutput(toolOutput);
            next = [
              ...next,
              {
                role: 'tool',
                content: `Tool ${toolMeta.tool} executed.`,
                toolMeta,
              }
            ];
          });
        }

        return next;
      });

      handleToolSideEffects(data.tool_outputs);
    } catch (error) {
      setError(error.message);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please make sure the backend server is running and the agent is configured.' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-card">
        <div className="chatbot-header">
          <Bot size={24} />
          <h2>Housing Price Assistant</h2>
        </div>
        
        <div className="messages-container">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-icon">
                {message.role === 'user' && <User size={20} />}
                {message.role === 'assistant' && <Bot size={20} />}
                {message.role === 'tool' && <Wrench size={20} />}
              </div>
              <div className="message-content">
                {renderMessageContent(message)}
              </div>
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <div className="message-icon">
                <Bot size={20} />
              </div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {error && (
          <div className="chat-error">
            <AlertTriangle size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about housing prices..."
            disabled={loading}
            className="chat-input"
          />
          <button type="submit" disabled={loading || !input.trim()} className="send-button">
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
}

export default Chatbot;
