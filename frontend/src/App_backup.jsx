/* =========================================
   1. GLOBAL & LAYOUT
   ========================================= */
   body {
    background-color: #18181A;
    color: #FFFFFF;
    font-family: 'Inter', system-ui, sans-serif;
    margin: 0;
    padding: 20px;
    min-height: 100vh;
    box-sizing: border-box;
    overflow-y: auto;
  }
  
  .app-wrapper {
    display: flex;
    flex-direction: column;
    gap: 24px;
    max-width: 1600px;
    margin: 0 auto;
    width: 100%;
  }
  
  /* =========================================
     2. HEADER
     ========================================= */
  .app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #1a1a1c;
    border-radius: 20px;
    border: 1px solid #333;
    padding: 0 30px;
    height: 80px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    flex-shrink: 0;
  }
  
  .header-logo {
    font-size: 1.5rem;
    font-weight: 900;
    color: #fff;
    text-transform: uppercase;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
  }
  .header-logo span { color: #FFA55B; }
  
  .nav-links { display: flex; gap: 30px; }
  .nav-item {
    color: #888;
    font-weight: 700;
    text-decoration: none;
    font-size: 0.95rem;
    transition: color 0.2s;
    cursor: pointer;
  }
  .nav-item:hover, .nav-item.active { color: #fff; }
  
  /* =========================================
     3. SHARED UI ELEMENTS
     ========================================= */
  .dashboard-card {
    background-color: #202022;
    border-radius: 24px;
    padding: 24px;
    border: 1px solid #2A2A2E;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  }
  
  .section-title {
    font-size: 1.1rem;
    margin-bottom: 15px;
    color: #FFA55B;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
  }
  
  .primary-btn {
    background-color: #FFA55B;
    color: #18181A;
    border: none;
    padding: 16px 32px;
    border-radius: 50px;
    font-weight: 800;
    font-size: 1rem;
    cursor: pointer;
    transition: transform 0.2s;
  }
  .primary-btn:hover { transform: scale(1.05); }
  
  /* Standard Scrollbar Styling */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: #555; }
  
  /* =========================================
     4. HOME DASHBOARD LAYOUT (FIXED)
     ========================================= */
  .welcome-card {
    background: linear-gradient(135deg, #252529 0%, #18181A 100%);
    border-radius: 24px;
    padding: 40px;
    border: 1px solid #2A2A2E;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    margin-bottom: 20px;
    flex-shrink: 0;
  }
  .welcome-text h1 { font-size: 3rem; margin: 0; line-height: 1.1; color: #fff; }
  .welcome-text p { color: #888; margin-top: 8px; font-size: 1.1rem; }
  
  /* The Main Home Grid */
  .home-grid {
    display: grid;
    grid-template-columns: 1.1fr 0.95fr 0.95fr; /* 3 Columns */
    gap: 24px;
    align-items: start;
  }
  
  .home-column {
    display: flex;
    flex-direction: column;
    gap: 24px;
    min-width: 0;
  }
  
  /* --- THE FIX: Force a specific height on Home Page cards --- */
  .home-column .dashboard-card {
    height: 550px; /* <--- This prevents the collapse */
    min-height: 550px; 
  }
  
  /* Force the scroll area to fill the remaining space inside that 550px */
  .home-column .dashboard-card .scroll-area {
    flex-grow: 1;
    overflow-y: auto;
    height: 0;        /* CSS trick: allows flex-grow to define the real height */
    min-height: 0;
    padding-right: 8px;
  }
  
  /* Home List Items */
  .match-item {
    display: flex; justify-content: space-between; padding: 16px 0;
    border-bottom: 1px solid #333; font-size: 0.95rem;
  }
  .match-teams { font-weight: 600; color: #eee; }
  .match-time { color: #5E918D; font-weight: bold; }
  
  .order-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 14px; margin-bottom: 8px; background: #2A2A2E;
    border-radius: 12px; border-left: 3px solid transparent;
  }
  .order-row:hover { border-left-color: #5E918D; background: #303035; }
  .pick-info { display: flex; gap: 10px; font-weight: 600; color: #eee; }
  .pick-num { color: #666; width: 30px; }
  .team-needs { font-size: 0.75rem; color: #5E918D; background: #1a1a1e; padding: 4px 8px; border-radius: 6px; border: 1px solid #333; }
  
  .draft-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 14px; margin-bottom: 8px; background: #2A2A2E;
    border-radius: 12px; border-left: 4px solid transparent;
  }
  .draft-item:hover { border-left-color: #FFA55B; background: #303035; transform: translateX(2px); }
  
  .player-main { display: flex; align-items: center; gap: 12px; }
  .rank-badge {
    background: #18181A; color: #FFA55B; width: 28px; height: 28px;
    display: flex; justify-content: center; align-items: center;
    border-radius: 50%; font-weight: 800; font-size: 0.9rem; flex-shrink: 0;
  }
  .player-name { font-weight: 700; color: #fff; }
  .player-meta { text-align: right; }
  .school { display: block; color: #888; font-size: 0.75rem; }
  .pos-tag { color: #5E918D; font-size: 0.75rem; font-weight: bold; background: #1a1a1e; padding: 2px 6px; border-radius: 4px; }
  
  /* Stock Trends */
  .trend-badge { font-size: 0.75rem; font-weight: bold; padding: 2px 6px; border-radius: 4px; }
  .trend-up { color: #4ade80; background: rgba(74, 222, 128, 0.1); }
  .trend-down { color: #f87171; background: rgba(248, 113, 113, 0.1); }
  .trend-flat { color: #94a3b8; background: rgba(148, 163, 184, 0.1); }
  
  /* =========================================
     5. RANKINGS PAGE LAYOUT
     ========================================= */
  .split-layout {
    display: flex;
    gap: 24px;
    align-items: flex-start;
  }
  .conference-grid {
    flex-grow: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }
  .sidebar {
    width: 280px;
    flex-shrink: 0;
    position: sticky;
    top: 20px;
  }
  .sidebar-card {
    background-color: #1a1a1c;
    border-radius: 20px;
    border: 1px solid #333;
    padding: 20px;
    max-height: 85vh;
    overflow-y: auto;
  }
  
  .conference-card {
    background-color: #1a1a1c;
    border-radius: 20px;
    border: 1px solid #333;
    padding: 0 24px 24px 24px;
    max-height: 550px;
    overflow-y: auto;
  }
  .conference-header {
    position: sticky; top: 0; z-index: 10;
    background-color: #1a1a1c;
    padding: 20px 0 15px 0;
    border-bottom: 2px solid #333;
    margin-bottom: 15px;
    font-size: 1.5rem; font-weight: 900; color: #fff;
    display: flex; justify-content: space-between;
  }
  
  .team-row {
    display: flex; align-items: stretch;
    background-color: #252529;
    border-radius: 12px; overflow: hidden;
    height: 50px; margin-bottom: 10px;
    border: 1px solid #2A2A2E; flex-shrink: 0;
  }
  .rank-box {
    width: 50px; display: flex; justify-content: center; align-items: center;
    font-size: 1.2rem; font-weight: 900; color: #fff;
  }
  .team-info {
    flex-grow: 1; display: flex; justify-content: space-between; align-items: center;
    padding: 0 15px;
  }
  .team-name-large { font-weight: 700; color: #fff; }
  .stat-pill {
    background: #18181A; padding: 4px 10px; border-radius: 6px;
    font-size: 0.8rem; color: #888; font-weight: bold; border: 1px solid #333;
  }
  .havoc-score { color: #FFA55B; }
  
  /* =========================================
     6. PLAYER PROFILE STYLES
     ========================================= */
  .back-btn {
    display: inline-flex; align-items: center; gap: 8px;
    background: transparent; border: 1px solid #333; color: #888;
    padding: 8px 20px; border-radius: 30px; cursor: pointer;
    margin-bottom: 20px; font-weight: 700;
  }
  .back-btn:hover { background: #2A2A2E; color: #fff; }
  
  .player-hero {
    background: linear-gradient(135deg, #202022 0%, #1a1a1c 100%);
    border-radius: 24px; padding: 40px;
    display: flex; align-items: center; gap: 40px;
    border: 1px solid #333; margin-bottom: 30px;
    position: relative; overflow: hidden;
  }
  .player-avatar {
    width: 120px; height: 120px; border-radius: 50%;
    background-color: #333; display: flex; justify-content: center; align-items: center;
    font-size: 2rem; font-weight: 900; color: #555; border: 4px solid #18181A; flex-shrink: 0;
  }
  .player-details h1 { font-size: 3rem; margin: 0; line-height: 1; color: #fff; }
  .player-meta { display: flex; gap: 15px; margin-top: 15px; color: #888; }
  .meta-tag { background: #18181A; padding: 6px 14px; border-radius: 8px; border: 1px solid #333; color: #FFA55B; }
  
  .player-stats-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px;
  }
  .stat-card {
    background-color: #202022; border-radius: 20px; padding: 24px;
    border: 1px solid #2A2A2E; display: flex; flex-direction: column; gap: 10px;
  }
  .stat-header { color: #888; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; }
  .stat-value-big { font-size: 2.2rem; font-weight: 800; color: #fff; }
  .stat-label { color: #5E918D; font-size: 0.9rem; font-weight: bold; }
  
  /* =========================================
     7. RESPONSIVE
     ========================================= */
  @media (max-width: 1200px) {
    .home-grid { grid-template-columns: 1fr; }
    .split-layout { flex-direction: column; }
    .sidebar { width: 100%; max-height: 400px; }
    .player-stats-grid { grid-template-columns: 1fr; }
    .player-hero { flex-direction: column; text-align: center; }
  }