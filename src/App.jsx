import React, { useState } from 'react';
import Navbar from './components/Navbar';
import IntroPage from './components/IntroPage';
import ChatInterface from './components/ChatInterface';
import DeveloperPage from './components/DeveloperPage';
import AboutElsa from './components/AboutElsa';
import MoviesPage from './components/MoviesPage';

function App() {
  const [currentPage, setCurrentPage] = useState('intro');

  const renderPage = () => {
    switch (currentPage) {
      case 'chat':
        return <ChatInterface />;
      case 'about-dev':
        return <DeveloperPage />;
      case 'about-elsa':
        return <AboutElsa />;
      case 'frozen-movies':
        return <MoviesPage />;
      case 'intro':
      default:
        return <IntroPage onStartChat={() => setCurrentPage('chat')} />;
    }
  };

  return (
    <div className="App">
      <Navbar setCurrentPage={setCurrentPage} currentPage={currentPage} />
      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;