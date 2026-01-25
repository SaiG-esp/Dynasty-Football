import React from 'react';
import './Header.css';

const Header = ({ setView, currentView }) => {
  return (
    <header className="app-header">
      <div 
        className="header-logo" 
        onClick={() => setView('home')} 
        style={{cursor: 'pointer'}}
      >
        Dynasty<span>CFB</span>
      </div>
      <div className="nav-links">
        <a 
          onClick={() => setView('rankings')} 
          className={`nav-item ${currentView === 'rankings' ? 'active' : ''}`}
        >
          Defensive Rankings
        </a>
        
        {/* --- WIRED UP THE MATCHUPS BUTTON --- */}
        <a 
          onClick={() => setView('matchups')} 
          className={`nav-item ${currentView === 'matchups' ? 'active' : ''}`}
        >
          Matchups
        </a>

        <a 
          onClick={() => setView('players')} 
          className={`nav-item ${currentView === 'players' ? 'active' : ''}`}
        >
          Players
        </a>
      </div>
    </header>
  );
};

export default Header;