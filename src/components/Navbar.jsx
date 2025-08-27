// src/components/Navbar.jsx
import React from 'react';
import { Home, MessageCircle, User, Film, User2 } from 'lucide-react';
import './Navbar.css';

const Navbar = ({ currentPage, setCurrentPage }) => {
  const menuItems = [
    { id: 'intro', label: 'Home', icon: Home },
    { id: 'chat', label: 'Chat with Elsa', icon: MessageCircle },
    { id: 'about-dev', label: 'Developer', icon: User }, // Changed from 'developer'
    { id: 'frozen-movies', label: 'Frozen Movies', icon: Film }, // Changed from 'movies'
    { id: 'about-elsa', label: 'About Elsa', icon: User2 } // Changed from 'elsa'
  ];

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <div className="navbar-logo">
          <span className="logo-icon">❄️</span>
          <span className="logo-text">Elsa AI</span>
        </div>
        <ul className="navbar-menu">
          {menuItems.map((item) => {
            const IconComponent = item.icon;
            return (
              <li key={item.id} className="nav-item">
                <button 
                  className={`nav-link ${currentPage === item.id ? 'active' : ''}`}
                  onClick={() => setCurrentPage(item.id)}
                >
                  <IconComponent className="nav-icon" size={20} />
                  <span className="nav-label">{item.label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;