import { SEC_TEAMS } from '../data/mockData.js'

function DefensiveRankings() {
  return (
    <div className="dashboard-container" style={{height: 'auto', overflow: 'visible'}}>
      {/* Note: We override the container height to let the page scroll */}
      
      <div className="rankings-container">
        
        {/* === CARD 1: SEC === */}
        <div className="conference-card">
          <div className="conference-header">
            <div>SEC <span style={{color:'#666', fontSize:'1rem'}}>Conference</span></div>
            <div style={{fontSize:'0.9rem', color:'#888', fontWeight:'normal'}}>Avg Havoc: 14.2%</div>
          </div>

          {SEC_TEAMS.map((team) => (
            <div key={team.rank} className="team-row">
              {/* Rank Box */}
              <div className="rank-box" style={{ backgroundColor: team.color }}>
                {team.rank}
              </div>
              {/* Info */}
              <div className="team-info">
                <div className="team-name-large">{team.name}</div>
                <div style={{display:'flex', gap:'10px'}}>
                   <div className="stat-pill">Rec: {team.record}</div>
                   <div className="stat-pill">PA: <span style={{color: '#fff'}}>{team.ppg}</span></div>
                   <div className="stat-pill">Havoc: <span className="havoc-score">{team.havoc}</span></div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* === PLACEHOLDER FOR NEXT CONFERENCE (Example) === */}
        {/* <div className="conference-card">
           <div className="conference-header">Big 10</div>
           ... list goes here ...
        </div> 
        */}

      </div>
    </div>
  )
}

export default DefensiveRankings