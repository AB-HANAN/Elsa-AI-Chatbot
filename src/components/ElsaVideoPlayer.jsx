import React from 'react';
import './ElsaVideoPlayer.css';

const ElsaVideoPlayer = ({ expression }) => {
  const getExpressionEmoji = () => {
    switch(expression) {
      case 'thinking': return '🤔';
      case 'speaking': return '😊';
      case 'sad': return '😢';
      default: return '❄️';
    }
  };
  
  return (
    <div className="elsa-video-container">
      <div className="elsa-avatar">
        <div className="elsa-face">
          <span className="elsa-expression">{getExpressionEmoji()}</span>
        </div>
        <div className="elsa-name">Queen Elsa</div>
      </div>
      <div className="ice-crystals">
        {Array.from({ length: 8 }, (_, i) => (
          <div key={i} className={`crystal crystal-${i + 1}`}>✦</div>
        ))}
      </div>
    </div>
  );
};

export default ElsaVideoPlayer;