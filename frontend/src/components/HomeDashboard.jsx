import React from 'react';
import './HomeDashboard.css';
import { CFP_MATCHUPS, BOWL_GAMES, FIRST_ROUND_ORDER, PROSPECTS_2026 } from '../data';

const HomeDashboard = ({ setView }) => {
  return (
    <div className="home-dashboard">
      
      {/* 1. HERO BANNER */}
      <div className="welcome-card">
        <div className="welcome-text">
          <h1>Dynasty Scout</h1>
          <p>Your War Room for the 2026 Rookie Draft.</p>
        </div>
        <button className="primary-btn" onClick={() => setView('rankings')}>
          Analyze Defense &rarr;
        </button>
      </div>

      {/* 2. MAIN GRID */}
      <div className="home-grid">
        
        {/* COL 1: GAMES (Auto Height) */}
        <div className="home-column">
          <div className="dashboard-card auto-height"> 
            <div className="section-title">🏆 CFP Bracket</div>
            <div className="scroll-area">
              {CFP_MATCHUPS.map((game) => (
                <div key={game.id} className="match-item">
                  <div className="match-teams">{game.home} vs {game.away}</div>
                  <div className="match-time">{game.date}</div>
                </div>
              ))}
            </div>
          </div>
          <div className="dashboard-card auto-height">
            <div className="section-title">🏈 Bowl Season</div>
            <div className="scroll-area">
              {BOWL_GAMES.map((game) => (
                <div key={game.id} className="match-item">
                  <div className="match-teams">{game.home} vs {game.away}</div>
                  <div className="match-time">{game.date}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* COL 2: DRAFT ORDER (Fixed Height) */}
        <div className="home-column">
          <div className="dashboard-card fixed-height">
            <div className="section-title">⚖️ NFL Draft Order</div>
            <div className="scroll-area">
              {FIRST_ROUND_ORDER.map((item) => (
                <div key={item.pick} className="order-row">
                  <div className="pick-info">
                    <span className="pick-num">#{item.pick}</span>
                    <span className="team-name">{item.team}</span>
                  </div>
                  <span className="team-needs">{item.needs}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* COL 3: BIG BOARD (Fixed Height) */}
        <div className="home-column">
          <div className="dashboard-card fixed-height">
            <div className="section-title">🔥 Offensive Big Board</div>
            <div className="scroll-area">
              {PROSPECTS_2026.map((p, index) => (
                <div key={p.id} className="draft-item">
                  <div className="player-main">
                    <div className="rank-badge">{index + 1}</div>
                    <div className="player-name">{p.name}</div>
                  </div>
                  
                  {/* Stock Trend Badges */}
                  <div className={`trend-badge trend-${p.trend || 'flat'}`}>
                    {p.trend === 'up' && 'Rise'}
                    {p.trend === 'down' && 'Fall'}
                    {p.trend === 'flat' && 'Stable'}
                  </div>

                  <div className="player-meta">
                    <span className="school">{p.school}</span>
                    <span className="pos-tag">{p.pos}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default HomeDashboard;