import React from 'react';
import './IntroPage.css';

const IntroPage = ({ onStartChat }) => {
  return (
    <div className="intro-page">
      {/* Animated snowflakes background */}
      <div className="snowflakes" aria-hidden="true">
        <div className="snowflake">❆</div>
        <div className="snowflake">❅</div>
        <div className="snowflake">❆</div>
        <div className="snowflake">❅</div>
        <div className="snowflake">❆</div>
        <div className="snowflake">❅</div>
        <div className="snowflake">❆</div>
        <div className="snowflake">❅</div>
      </div>
      
      <div className="intro-content">
        <div className="intro-header">
          <div className="sparkle-icon">
            <i className="fas fa-snowflake intro-icon"></i>
          </div>
          <h1 className="magical-title">
            <span className="title-part">Queen</span>
            <span className="title-part">Elsa</span>
            <span className="title-part">of</span>
            <span className="title-part">Arendelle</span>
          </h1>
          <p className="intro-subtitle">The Snow Queen awaits your conversation</p>
        </div>
        
        <div className="intro-features">
          <div className="feature">
            <div className="feature-icon">
              <i className="fas fa-comment-alt"></i>
            </div>
            <h3>Magical Conversations</h3>
            <p>Chat with Elsa about her powers, kingdom, and adventures</p>
          </div>
          
          <div className="feature">
            <div className="feature-icon">
              <i className="fas fa-crown"></i>
            </div>
            <h3>Royal Wisdom</h3>
            <p>Get insights from the Queen of Arendelle herself</p>
          </div>

        </div>

        <div className="frost-effect">
          <button className="snowman-btn" onClick={onStartChat}>
            <span className="btn-sparkle">✨</span>
            <i className="fas fa-snowman"></i>
            Do you want to build a snowman?
            <span className="btn-sparkle">✨</span>
          </button>
        </div>
        
        <div className="intro-footer">
          <p>Powered by magic and machine learning ❄️</p>
        </div>
      </div>
    </div>
  );
};

export default IntroPage;