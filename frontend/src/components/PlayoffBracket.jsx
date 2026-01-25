import React from 'react';
import './PlayoffBracket.css';

// Data remains the same
const bracketData = {
  firstRound: [
    { id: 1, home: 'Oregon', seed: 5, score: 51, away: 'James Madison', awaySeed: 12, awayScore: 34 },
    { id: 2, home: 'Texas Tech', seed: 4, score: '-', away: 'BYE', awaySeed: '', awayScore: '' },
    { id: 3, home: 'Alabama', seed: 9, score: 34, away: 'Oklahoma', awaySeed: 8, awayScore: 24 },
    { id: 4, home: 'Indiana', seed: 1, score: '-', away: 'BYE', awaySeed: '', awayScore: '' },
    { id: 5, home: 'Ole Miss', seed: 6, score: 41, away: 'Tulane', awaySeed: 11, awayScore: 10 },
    { id: 6, home: 'Georgia', seed: 3, score: '-', away: 'BYE', awaySeed: '', awayScore: '' },
    { id: 7, home: 'Miami', seed: 10, score: 10, away: 'Texas A&M', awaySeed: 7, awayScore: 3 },
    { id: 8, home: 'Ohio State', seed: 2, score: '-', away: 'BYE', awaySeed: '', awayScore: '' },
  ],
  quarterfinals: [
    { id: 9, home: 'Oregon', seed: 5, score: 23, away: 'Texas Tech', awaySeed: 4, awayScore: 0 },
    { id: 10, home: 'Indiana', seed: 1, score: 38, away: 'Alabama', awaySeed: 9, awayScore: 3 },
    { id: 11, home: 'Ole Miss', seed: 6, score: 39, away: 'Georgia', awaySeed: 3, awayScore: 34 },
    { id: 12, home: 'Miami', seed: 10, score: 24, away: 'Ohio State', awaySeed: 2, awayScore: 14 },
  ],
  semifinals: [
    { id: 13, home: 'Indiana', seed: 1, score: 56, away: 'Oregon', awaySeed: 5, awayScore: 22 },
    { id: 14, home: 'Miami', seed: 10, score: 31, away: 'Ole Miss', awaySeed: 6, awayScore: 27 },
  ],
  championship: [
    { id: 15, home: 'Indiana', seed: 1, score: 27, away: 'Miami', awaySeed: 10, awayScore: 21 },
  ]
};

const MatchCard = ({ match }) => {
  if (match.away === 'BYE') {
     return (
        <div className="match-card bye-card">
            <div className="team-slot winner">
                <div style={{display:'flex', gap:'8px'}}>
                  <span className="seed">{match.seed}</span>
                  <span className="team-name">{match.home}</span>
                </div>
                <span className="score">BYE</span>
            </div>
        </div>
     );
  }

  const homeWin = parseInt(match.score) > parseInt(match.awayScore);
  const awayWin = parseInt(match.awayScore) > parseInt(match.score);

  return (
    <div className="match-card">
      <div className={`team-slot ${homeWin ? 'winner' : 'loser'}`}>
        <div style={{display:'flex', gap:'6px'}}>
            <span className="seed">{match.seed}</span>
            <span className="team-name">{match.home}</span>
        </div>
        <span className="score">{match.score}</span>
      </div>
      <div className="match-divider"></div>
      <div className={`team-slot ${awayWin ? 'winner' : 'loser'}`}>
        <div style={{display:'flex', gap:'6px'}}>
            <span className="seed">{match.awaySeed}</span>
            <span className="team-name">{match.away}</span>
        </div>
        <span className="score">{match.awayScore}</span>
      </div>
    </div>
  );
};

const PlayoffBracket = () => {
  return (
    <div className="bracket-container">
      <div className="bracket-header">
        <h1>2025 CFP Bracket</h1>
        <span className="bracket-subtitle">Road to the Championship</span>
      </div>

      <div className="bracket-grid">
        
        {/* ROUND 1 */}
        <div className="round-column">
            <h3>First Round</h3>
            {bracketData.firstRound.map(m => <MatchCard key={m.id} match={m} />)}
        </div>

        {/* CONNECTOR 1 (4 Forks) */}
        <div className="connector-column">
            <div className="bracket-fork"></div>
            <div className="bracket-fork"></div>
            <div className="bracket-fork"></div>
            <div className="bracket-fork"></div>
        </div>

        {/* QUARTERFINALS */}
        <div className="round-column">
            <h3>Quarterfinals</h3>
            {bracketData.quarterfinals.map(m => <MatchCard key={m.id} match={m} />)}
        </div>

        {/* CONNECTOR 2 (2 Forks) */}
        <div className="connector-column">
            <div className="bracket-fork"></div>
            <div className="bracket-fork"></div>
        </div>

        {/* SEMIFINALS */}
        <div className="round-column">
            <h3>Semifinals</h3>
            {bracketData.semifinals.map(m => <MatchCard key={m.id} match={m} />)}
        </div>

        {/* CONNECTOR 3 (1 Fork) */}
        <div className="connector-column">
            <div className="bracket-fork"></div>
        </div>

        {/* CHAMPIONSHIP */}
        <div className="round-column championship-column">
            <h3>National Title</h3>
            <div className="trophy-icon">🏆</div>
            {bracketData.championship.map(m => <MatchCard key={m.id} match={m} />)}
        </div>

      </div>
    </div>
  );
};

export default PlayoffBracket;