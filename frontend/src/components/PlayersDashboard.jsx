import React, { useState } from 'react';
import './PlayersDashboard.css';
import { PLAYER_DATABASE } from '../data'; // <--- Using the Big Database

const PlayersDashboard = ({ onPlayerClick }) => {
  const [activeTab, setActiveTab] = useState('ALL');
  const [searchTerm, setSearchTerm] = useState('');

  // SAFETY: If data is missing, default to empty array
  const safePlayers = PLAYER_DATABASE || [];

  // Filter Logic
  const filteredPlayers = safePlayers.filter(p => {
    // 1. Tab Filter
    const matchesTab = activeTab === 'ALL' 
      ? true 
      : p.pos && p.pos.includes(activeTab); 

    // 2. Search Filter
    // Ensure name/school exist before lowercasing to avoid crash
    const nameMatch = p.name ? p.name.toLowerCase().includes(searchTerm.toLowerCase()) : false;
    const schoolMatch = p.school ? p.school.toLowerCase().includes(searchTerm.toLowerCase()) : false;

    return matchesTab && (nameMatch || schoolMatch);
  });

  return (
    <div className="players-dashboard">
      
      {/* Header */}
      <div className="players-header-row">
        <h1 className="page-title">2026 Draft Class Database</h1>
        <div className="search-wrapper">
          <input 
            type="text" 
            placeholder="Search Player or School..." 
            className="player-search"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="filter-row">
        {['ALL', 'QB', 'RB', 'WR', 'TE'].map(type => (
          <button 
            key={type}
            className={`filter-pill ${activeTab === type ? 'active' : ''}`}
            onClick={() => setActiveTab(type)}
          >
            {type}
          </button>
        ))}
      </div>

      {/* The Table */}
      <div className="table-container">
        {filteredPlayers.length > 0 ? (
          <table className="players-table">
            <thead>
              <tr>
                <th className="th-rank">#</th>
                <th className="th-player">PLAYER</th>
                <th className="th-team">SCHOOL</th>
                <th className="th-stat">YDS</th>
                <th className="th-stat">TD</th>
                <th className="th-stat">AVG</th>
                <th className="th-trend">TREND</th>
              </tr>
            </thead>
            <tbody>
              {filteredPlayers.map((player, index) => {
                // Fallback to '-' if missing
                const s1 = player.stats?.s1 || '-';
                const s2 = player.stats?.s2 || '-';
                const s3 = player.stats?.s3 || '-';

                return (
                  <tr key={player.id} onClick={() => onPlayerClick(player.id)}>
                    <td className="td-rank">{index + 1}</td>
                    <td className="td-player">
                      <div className="player-cell">
                        <div className="player-avatar-small">
                          {player.name ? player.name.charAt(0) : '?'}
                        </div>
                        <div className="player-info">
                          <span className="p-name">{player.name}</span>
                          <span className="p-pos">{player.pos}</span>
                        </div>
                      </div>
                    </td>
                    <td className="td-team">
                      <span className="team-pill">{player.school}</span>
                    </td>
                    
                    <td className="td-stat">{s1}</td>
                    <td className="td-stat">{s2}</td>
                    <td className="td-stat">{s3}</td>
                    
                    <td className="td-trend">
                      <span className={`trend-tag ${player.trend || 'flat'}`}>
                        {player.trend === 'up' ? '▲' : player.trend === 'down' ? '▼' : '-'}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        ) : (
          <div style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
            <h2>No players found.</h2>
            <p>Try adjusting your search or filters.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PlayersDashboard;