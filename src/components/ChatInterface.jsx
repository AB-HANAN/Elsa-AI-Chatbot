import React, { useState, useEffect, useRef } from 'react';
import { sendMessage as sendMessageToAPI } from '../services/api';
import './ChatInterface.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: "Hello! I'm Elsa, the Snow Queen of Arendelle. How can I help you today?",
      time: 'Just now',
      isError: false
    }
  ]);
  const [userInput, setUserInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [charCount, setCharCount] = useState(0);
  const [isSending, setIsSending] = useState(false);
  const chatBoxRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    // Add Font Awesome to the document head
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
    document.head.appendChild(link);

    inputRef.current?.focus();

    // Cleanup
    return () => {
      document.head.removeChild(link);
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const formatMessage = (text) => {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/_(.*?)_/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code>$1</code>')
      .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
      .replace(/\n/g, '<br>');
  };

  const addMessage = (text, sender, isError = false) => {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const currentTime = `${hours}:${minutes}`;

    const newMessage = {
      id: Date.now(),
      sender,
      text,
      time: currentTime,
      isError
    };

    setMessages(prev => [...prev, newMessage]);
  };

  const scrollToBottom = () => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: Date.now(),
        sender: 'bot',
        text: "Chat cleared! How can I help you today?",
        time: 'Just now',
        isError: false
      }
    ]);
  };

  const handleInputChange = (e) => {
    const text = e.target.value;
    setUserInput(text);
    setCharCount(text.length);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const sendMessage = async () => {
    const message = userInput.trim();
    if (!message) return;

    // Add user message
    addMessage(message, 'user');
    setUserInput('');
    setCharCount(0);
    
    // Show typing indicator and disable send button
    setIsTyping(true);
    setIsSending(true);
    
    try {
      // Use the API service instead of direct fetch
      const response = await sendMessageToAPI(message);
      
      // Hide typing indicator and add response
      setTimeout(() => {
        setIsTyping(false);
        setIsSending(false);
        addMessage(response, 'bot');
      }, 800);
      
    } catch (error) {
      setIsTyping(false);
      setIsSending(false);
      addMessage(`Connection error: ${error.message}. Please try again.`, 'bot', true);
    }
  };

  const handleAttachmentClick = (e) => {
    e.preventDefault();
    console.log('Attachment feature - coming soon!');
  };

  const getCharCountColor = () => {
    if (charCount > 800) return '#fc8181';
    if (charCount > 600) return '#f6ad55';
    return '#718096';
  };

  return (
    <div className="chat-container">
      {/* Header */}
      <div className="chat-header">
        <div className="header-left">
          <div className="bot-avatar">
            <i className="fas fa-snowflake snowflake-icon"></i>
          </div>
          <div className="header-info">
            <h1>Queen Elsa</h1>
            <p className="status">
              <span className="status-dot"></span>
              Online - Queen of Arendelle
            </p>
          </div>
        </div>
        <div className="header-actions">
          <button className="action-btn" onClick={clearChat} title="Clear Chat">
            <i className="fas fa-trash"></i>
          </button>
          {/* REMOVED: Theme toggle button */}
        </div>
      </div>

      {/* Chat Messages */}
      <div className="chat-messages" ref={chatBoxRef}>
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.sender}-message ${message.isError ? 'error' : ''}`}>
            <div className="message-avatar">
              {message.sender === 'user' ? (
                <i className="fas fa-user"></i>
              ) : (
                <i className="fas fa-snowflake snowflake-icon"></i>
              )}
            </div>
            <div className="message-content">
              <div className="message-bubble">
                <p dangerouslySetInnerHTML={{ __html: formatMessage(message.text) }} />
              </div>
              <div className="message-time">{message.time}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Typing Indicator */}
      {isTyping && (
        <div className="typing-indicator">
          <div className="message bot-message">
            <div className="message-avatar">
              <i className="fas fa-snowflake snowflake-icon"></i>
            </div>
            <div className="message-content">
              <div className="message-bubble">
                <div className="typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
              <div className="message-time">Typing...</div>
            </div>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="chat-input">
        <div className="input-container">
          <button className="attachment-btn" onClick={handleAttachmentClick} title="Attach File">
            <i className="fas fa-paperclip"></i>
          </button>
          <input 
            ref={inputRef}
            type="text" 
            value={userInput}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here..." 
            autoComplete="off"
            maxLength="1000"
          />
          <button 
            className="send-btn" 
            onClick={sendMessage} 
            title="Send Message"
            disabled={isSending}
          >
            <i className={isSending ? 'fas fa-circle-notch fa-spin' : 'fas fa-paper-plane'}></i>
          </button>
        </div>
        <div className="input-footer">
          <span className="char-count" style={{ color: getCharCountColor() }}>
            {charCount}/1000
          </span>
          <span className="ai-notice">Elsa's responses may contain magic. Please verify important information.</span>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;