import { Link } from 'react-router-dom'
import { PROSPECTS_2025, CFP_MATCHUPS, BOWL_GAMES, FIRST_ROUND_ORDER } from '../data/mockData.js'

function Home() {
  return (
    <div className="dashboard-container">
      
      {/* 1. TOP ROW: Welcome Header */}
      <div className="welcome-card">
        <div className="welcome-text">
          <h1>Dynasty Scout</h1>
          <p>Your War Room for the 2025 Rookie Draft.</p>
        </div>
        <Link to="/rankings">
          <button className="primary-btn">Analyze Defense &rarr;</button>
        </Link>
      </div>

      {/* 2. BOTTOM ROW: 3 Columns */}
      <div className="content-grid">
        
        {/* COLUMN 1: MATCHUPS (Split Top/Bottom) */}
        <div className="column">
          {/* Top Half: CFP Bracket */}
          <div className="dashboard-card" style={{flex: 1}}>
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

          {/* Bottom Half: Bowl Games */}
          <div className="dashboard-card" style={{flex: 1}}>
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

        {/* COLUMN 2: NFL DRAFT ORDER */}
        <div className="column">
          <div className="dashboard-card">
            <div className="section-title">⚖️ NFL Draft Order</div>
            <div className="scroll-area">
              {FIRST_ROUND_ORDER.map((item) => (
                <div key={item.pick} className="order-row">
                  {/* LEFT SIDE: Rank + Name */}
                  <div className="pick-info">
                    <span className="pick-num">#{item.pick}</span>
                    <span className="team-name">{item.team}</span>
                  </div>
                  {/* RIGHT SIDE: Needs */}
                  <div className="team-needs">Needs: {item.needs}</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* COLUMN 3: ROOKIE BIG BOARD (With Stock Watch) */}
        <div className="column">
          <div className="dashboard-card">
            <div className="section-title">🔥 Offensive Big Board</div>
            <div className="scroll-area">
              {PROSPECTS_2025.map((p, index) => (
                <div key={p.id} className="draft-item">
                  
                  {/* 1. LEFT: Rank + Name */}
                  <div className="player-main">
                    <div className="rank-badge">{index + 1}</div>
                    <div className="player-name">{p.name}</div>
                  </div>

                  {/* 2. CENTER: Stock Trend Indicator (Fills the gap) */}
                  {/* Using conditional logic to show the right badge */}
                  {p.trend === 'up' && <div className="trend-badge trend-up">🔥 Rise</div>}
                  {p.trend === 'down' && <div className="trend-badge trend-down">❄️ Fall</div>}
                  {p.trend === 'flat' && <div className="trend-badge trend-flat">➖ Stable</div>}
                  {/* Fallback if trend is missing */}
                  {!p.trend && <div className="trend-badge trend-flat">➖ Stable</div>}

                  {/* 3. RIGHT: School + Pos */}
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
  )
}

export default Home