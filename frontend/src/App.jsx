import React, { useState } from 'react';

import Header from './components/Header';
import HomeDashboard from './components/HomeDashboard';
import RankingsDashboard from './components/RankingsDashboard';
import PlayerProfile from './components/PlayerProfile';
import PlayersDashboard from './components/PlayersDashboard';
import PlayoffBracket from './components/PlayoffBracket';

import { PLAYER_DATABASE } from './data';

function App() {
  const [view, setView] = useState('home');
  const [selectedPlayer, setSelectedPlayer] = useState(null);

  const handlePlayerClick = (id) => {
    const found = (PLAYER_DATABASE || []).find((p) => String(p.id) === String(id));
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
