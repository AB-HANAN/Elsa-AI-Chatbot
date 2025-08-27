// src/services/api.js
const API_BASE_URL = 'http://localhost:5000';

export const sendMessage = async (message) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });
    
    if (!response.ok) {
      throw new Error('Failed to send message');
    }
    
    const data = await response.json();
    
    if (data.error) {
      throw new Error(data.error);
    }
    
    return data.response;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};