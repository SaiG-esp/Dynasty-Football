import React, { useState, useEffect } from 'react';
import './styles/global.css';

// Components
import Header from './components/Header';
import HomeDashboard from './components/HomeDashboard';
import RankingsDashboard from './components/RankingsDashboard';
import PlayerProfile from './components/PlayerProfile';
import PlayersDashboard from './components/PlayersDashboard';
import PlayoffBracket from './components/PlayoffBracket'; // <--- 1. NEW IMPORT

// Data
import { samplePlayers, PROSPECTS_2025, PLAYER_DATABASE } from './data';

function App() {
  const [view, setView] = useState('home');
  const [selectedPlayer, setSelectedPlayer] = useState(null);

  // Debug: Check if data is loaded on startup
  useEffect(() => {
    console.log("App Loaded.");
    console.log("Big DB Size:", PLAYER_DATABASE ? PLAYER_DATABASE.length : 0);
    console.log("Curated DB Size:", PROSPECTS_2025 ? PROSPECTS_2025.length : 0);
  }, []);

  const handlePlayerClick = (id) => {
    console.log("🖱️ User clicked Player ID:", id, "(Type:", typeof id, ")");

    // 1. SAFE SEARCH: Convert everything to Strings to prevent Type mismatch
    const searchId = String(id);
    
    // Check Big Database
    let found = (PLAYER_DATABASE || []).find(p => String(p.id) === searchId);
    
    // Check Curated List
    if (!found) {
        found = (PROSPECTS_2025 || []).find(p => String(p.id) === searchId);
    }

    // Check Sample Data (Fallback)
    if (!found && samplePlayers[searchId]) {
        found = samplePlayers[searchId];
    }

    if (found) {
      console.log("✅ Found Player:", found.name);
      setSelectedPlayer(found);
      setView('player');
    } else {
      console.warn("❌ Player NOT found! Check if IDs match.");
      alert(`Debug: Could not find player with ID: ${id}`);
    }
  };

  return (
    <div className="app-wrapper">
      <Header setView={setView} currentView={view} />
      
      <div className="main-content-area">
        {view === 'home' && <HomeDashboard setView={setView} />}
        {view === 'rankings' && <RankingsDashboard />}
        
        {/* <--- 2. NEW VIEW ADDITION ---> */}
        {view === 'matchups' && <PlayoffBracket />}
        
        {view === 'players' && (
          <PlayersDashboard onPlayerClick={handlePlayerClick} />
        )}

        {view === 'player' && (
          <PlayerProfile 
            player={selectedPlayer} 
            onBack={() => setView('players')} 
          />
        )}
      </div>
    </div>
  );
}

export default App;