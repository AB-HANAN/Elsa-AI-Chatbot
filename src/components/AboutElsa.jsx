import React from 'react';
import './AboutElsa.css';

const AboutElsa = () => {
  return (
    <div className="about-page">
      <div className="about-content">
        <div className="title-container">
          <h1 className="vibrant-title">
            <span className="title-word title-word-1">About</span>
            <span className="title-word title-word-2">Elsa</span>
          </h1>
          <div className="title-subtext">The Snow Queen of Arendelle ❄️</div>

          {/* Animated snowflakes */}
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
        </div>

        <div className="about-card">
          <h2>The Snow Queen of Arendelle</h2>
          <p>
            Elsa is the beloved queen with magical ice powers from Disney's Frozen franchise. 
            She possesses the ability to create and control ice and snow, symbolizing beauty, strength, and independence.
          </p>

          <h3>What to Expect:</h3>
          <ul>
            <li>Conversations about her magical abilities and kingdom</li>
            <li>Insights into her relationship with sister Anna</li>
            <li>Stories about her adventures and challenges</li>
            <li>Royal wisdom and leadership perspectives</li>
            <li>Discussions about ice magic and winter</li>
          </ul>

          <h3>Personality Traits:</h3>
          <p>
            Elsa is compassionate, responsible, and thoughtful. She speaks with regal elegance 
            and has a warm heart beneath her initially reserved exterior.
          </p>

          <h3>Her Magical Powers:</h3>
          <ul>
            <li>Creating blizzards and snowstorms</li>
            <li>Building ice castles and sculptures instantly</li>
            <li>Breathing life into snow creatures like Olaf</li>
            <li>Summoning protective ice barriers</li>
          </ul>

          <h3>Famous Quote:</h3>
          <p className="fun-note">
            <em>"Let it go, let it go! Can’t hold it back anymore."</em>
          </p>

          <h3>Fun Fact:</h3>
          <p>
            Elsa is one of Disney’s few queens who rules alone, symbolizing independence 
            and empowerment for audiences worldwide.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AboutElsa;
