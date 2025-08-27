import React from 'react';
import './MoviesPage.css';

const MoviesPage = () => {
  const movies = [
    {
      title: "Frozen (2013)",
      description: "The original adventure where Elsa accidentally unleashes an eternal winter on Arendelle",
      image: "❄️"
    },
    {
      title: "Frozen Fever (2015)",
      description: "A short film following Elsa's attempts to give Anna the perfect birthday",
      image: "🎂"
    },
    {
      title: "Frozen II (2019)",
      description: "Elsa and Anna journey to the enchanted forests to discover the origin of Elsa's powers",
      image: "🌲"
    }
  ];

  return (
    <div className="movies-page">
      {/* ❄️ Snowflake background */}
      <div className="snowflakes" aria-hidden="true">
        <div className="snowflake">❄</div>
        <div className="snowflake">✦</div>
        <div className="snowflake">❄</div>
        <div className="snowflake">✦</div>
        <div className="snowflake">❄</div>
      </div>

      <div className="movies-content">
        <h1 className="icy-title">❄️ Frozen Movies Collection 🧊</h1>
        
        <div className="movies-grid">
          {movies.map((movie, index) => (
            <div key={index} className="movie-card">
              <div className="movie-icon">{movie.image}</div>
              <h3>{movie.title}</h3>
              <p>{movie.description}</p>
            </div>
          ))}
        </div>

        <div className="movies-info">
          <h2>About the Franchise</h2>
          <p>
            The Frozen franchise has captivated audiences worldwide with its story of sisterly love, 
            self-discovery, and magical adventures. Elsa's journey from fear to self-acceptance has 
            become an inspiring tale for all ages.
          </p>
        </div>
      </div>
    </div>
  );
};

export default MoviesPage;
