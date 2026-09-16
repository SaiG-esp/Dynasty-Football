import React, { useState } from 'react';
import './styles/global.css';

import Header from './components/Header';
import HomeDashboard from './components/HomeDashboard';
import RankingsDashboard from './components/RankingsDashboard';
import PlayerProfile from './components/PlayerProfile';
import PlayersDashboard from './components/PlayersDashboard';
import PlayoffBracket from './components/PlayoffBracket';

import { samplePlayers, PROSPECTS_2026, PLAYER_DATABASE } from './data';

function App() {
  const [view, setView] = useState('home');
  const [selectedPlayer, setSelectedPlayer] = useState(null);

  const handlePlayerClick = (id) => {
    const searchId = String(id);

    let found = (PLAYER_DATABASE || []).find((p) => String(p.id) === searchId);

    if (!found) {
      found = (PROSPECTS_2026 || []).find((p) => String(p.id) === searchId);
    }

    if (!found && samplePlayers[searchId]) {
      found = samplePlayers[searchId];
    }

    if (found) {
      setSelectedPlayer(found);
      setView('player');
    }
  };

  return (
    <div className="app-wrapper">
      <Header setView={setView} currentView={view} />

      <div className="main-content-area">
        {view === 'home' && <HomeDashboard setView={setView} />}
        {view === 'rankings' && <RankingsDashboard />}
        {view === 'matchups' && <PlayoffBracket />}
        {view === 'players' && <PlayersDashboard onPlayerClick={handlePlayerClick} />}
        {view === 'player' && (
          <PlayerProfile player={selectedPlayer} onBack={() => setView('players')} />
        )}
      </div>
    </div>
  );
}

export default App;
