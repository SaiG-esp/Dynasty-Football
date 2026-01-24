import React from 'react';
import './RankingsDashboard.css';
import { conferenceData, apTop25Data } from '../data';

const TeamRow = ({ team, rank }) => (
  <div className="team-row">
    <div className="rank-box" style={{ backgroundColor: team.color, color: team.darkText ? '#000' : '#fff' }}>
      {rank}
    </div>
    <div className="team-info">
      <span className="team-name-large">{team.name}</span>
      <div style={{ display: 'flex', gap: '10px' }}>
        <span className="stat-pill havoc-score">Havoc: {team.havoc}</span>
        <span className="stat-pill">EPA: {team.epa}</span>
      </div>
    </div>
  </div>
);

const ConferenceCard = ({ title, teams }) => (
  <div className="conference-card">
    <div className="conference-header">
      <span>{title}</span>
      <span>{teams.length} Teams</span>
    </div>
    {teams.map((team, index) => <TeamRow key={team.name} rank={index + 1} team={team} />)}
  </div>
);

const RankingsDashboard = () => {
  return (
    <div className="split-layout">
      <div className="conference-grid">
        {conferenceData.map((conf) => (
          <ConferenceCard key={conf.name} title={conf.name} teams={conf.teams} />
        ))}
      </div>
      
      <div className="sidebar">
        <div className="sidebar-card">
          <div className="conference-header"><span>AP Top 25</span></div>
          {apTop25Data.map((team) => (
             <div key={team.name} className="team-row" style={{ height: '40px' }}>
                <div className="rank-box" style={{ backgroundColor: '#333', color: '#fff', width: '35px', fontSize: '0.9rem' }}>
                  {team.rank}
                </div>
                <div className="team-info" style={{ padding: '0 12px' }}>
                  <span className="team-name-large" style={{ fontSize: '0.9rem' }}>{team.name}</span>
                  <span style={{ color: '#666', fontSize: '0.8rem', fontWeight: 'bold' }}>{team.record}</span>
                </div>
             </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RankingsDashboard;