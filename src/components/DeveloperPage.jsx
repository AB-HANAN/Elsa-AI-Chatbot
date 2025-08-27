import React from 'react';
import './DeveloperPage.css';

const DeveloperPage = () => {
  return (
    <div className="about-page">
      <div className="about-content">
        <div className="title-container">
          <h1 className="vibrant-title">
            <span className="title-word title-word-1">The</span>
            <span className="title-word title-word-2">Magic</span>
            <span className="title-word title-word-3">Behind</span>
            <span className="title-word title-word-4">Elsa</span>
            <span className="title-word title-word-5">AI</span>
          </h1>
          <div className="title-subtext">A Frozen-Inspired Creation Story</div>
          <div className="snowflakes" aria-hidden="true">
            <div className="snowflake">❆</div>
            <div className="snowflake">❅</div>
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
          {/* ... rest of your content remains the same ... */}
          <h2>How Elsa AI Was Created</h2>
          <p>
            This AI chatbot was built using cutting-edge machine learning technology 
            fine-tuned specifically to capture Elsa's personality, knowledge, and mannerisms.
          </p>
          
          <h3>How It Started: A Sister's Wish ❄️</h3>
          <p>
            The developer was once approached by his sister who was watching Frozen Movie 
            (her favorite animated movie) on her tablet. Out of the blue, she asked her big brother: 
            <em>"Is there any way that I can talk to Elsa in real life?"</em>
          </p>
          
          <p>
            The developer thought, <em>"Hmmm... let's try it, shall we?"</em> And so the journey began!
          </p>

          <h3>Technical Stack:</h3>
          <ul>
            <li>React.js for the frontend interface</li>
            <li>Flask Python framework for the backend API</li>
            <li>Hugging Face Transformers for the AI model</li>
            <li>Fine-tuned TinyLLaMA model for authentic responses</li>
            <li>800+ lines of custom Elsa dialogues and Q&A pairs</li>
          </ul>

          <h3>The Development Journey:</h3>
          <p>
            Fast forward one week - Elsa AI was born! The project took:
          </p>
          <ul>
            <li>2-3 days of training (on a potato laptop! 🥔)</li>
            <li>2-3 days for frontend and backend development</li>
            <li>Countless cups of coffee ☕</li>
          </ul>

          <h3>Training Process:</h3>
          <p>
            The model was trained on extensive dialogue data from Frozen movies, 
            character analyses, and custom Q&A pairs to ensure authentic Elsa responses.
          </p>

          <h3>A Note on Authenticity:</h3>
          <p>
            <strong>Fun fact:</strong> Elsa might occasionally hallucinate or get creative with her responses! 
            This is because she was trained on a relatively small dataset (800+ lines) and runs on TinyLLaMA - 
            chosen because the developer had a potato laptop compared to the computational power this project deserved! 😄
          </p>
          
          <p className="fun-note">
            But hey, even magic has its limits! The important thing is that she captures the spirit 
            of the Snow Queen and can have meaningful conversations about winter, magic, and sisterly love.
          </p>
        </div>
      </div>
    </div>
  );
};

export default DeveloperPage;