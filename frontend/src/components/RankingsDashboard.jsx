import React, { useMemo } from 'react'; // Import useMemo for performance
import './RankingsDashboard.css';
import { conferenceData, apTop25Data } from '../data';

const TeamRow = ({ team, rank }) => (
  <div className="team-row">
    <div className="rank-box" style={{ backgroundColor: team.color || '#333', color: team.darkText ? '#000' : '#fff' }}>
      {rank}
    </div>
    <div className="team-info">
      <span className="team-name-large">{team.name}</span>
      <div style={{ display: 'flex', gap: '10px' }}>
        {/* Only show pills if the data exists, otherwise show 'N/A' or hide */}
        <span className="stat-pill havoc-score">
          Havoc: {team.havoc || '-'}
        </span>
        <span className="stat-pill">
          EPA: {team.epa || '-'}
        </span>
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
    <div className="table-container">
        {teams.map((team, index) => (
          <TeamRow 
            key={team.name} 
            rank={team.rank || index + 1} 
            team={team} 
          />
        ))}
    </div>
  </div>
);

const RankingsDashboard = () => {

  // --- THE FIX: SMART DATA MERGE ---
  // This creates a "Master List" of stats from all conferences
  const enrichedTop25 = useMemo(() => {
    // 1. Create a lookup dictionary: { "Oregon": { havoc: 95, epa: 0.5 }, ... }
    const statsLookup = {};
    
    conferenceData.forEach(conf => {
      conf.teams.forEach(team => {
        statsLookup[team.name] = { 
          havoc: team.havoc, 
          epa: team.epa,
          color: team.color // Grab the team color too!
        };
      });
    });

    // 2. Map over the AP Top 25 and inject the stats found in the dictionary
    return apTop25Data.map(apTeam => {
      const stats = statsLookup[apTeam.name];
      return {
        ...apTeam, // Keep existing AP data (Rank, Record)
        havoc: stats ? stats.havoc : '-', // Inject Havoc (or '-' if not found)
        epa: stats ? stats.epa : '-',     // Inject EPA
        color: stats ? stats.color : '#333' // Inject Team Color
      };
    });
  }, []); // Empty dependency array means this runs once on load

  return (
    <div className="dashboard-container">
      <div className="conference-grid">
        
        {/* Render the Enriched Top 25 List */}
        <ConferenceCard title="AP Top 25" teams={enrichedTop25} />

        {/* Render the rest of the conferences normally */}
        {conferenceData.map((conf) => (
          <ConferenceCard key={conf.name} title={conf.name} teams={conf.teams} />
        ))}

      </div>
    </div>
  );
};

export default RankingsDashboard;