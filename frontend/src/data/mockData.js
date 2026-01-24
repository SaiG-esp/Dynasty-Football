export const ROOKIES_2024 = [
    { id: 1, name: "Marvin Harrison Jr.", team: "ARI", pos: "WR", points: 14.2 },
    { id: 2, name: "Malik Nabers", team: "NYG", pos: "WR", points: 15.6 },
    { id: 3, name: "Jayden Daniels", team: "WAS", pos: "QB", points: 22.1 },
    { id: 4, name: "Brock Bowers", team: "LV", pos: "TE", points: 12.8 },
    { id: 5, name: "Brian Thomas Jr.", team: "JAX", pos: "WR", points: 13.5 },
];

// FILTERED: Only offensive skill positions (QB, RB, WR, TE)
// Travis Hunter stays because he plays WR. Mason Graham (DL) is removed.
// ... keep ROOKIES_2024 ...

export const PROSPECTS_2025 = [
    { id: 1, name: "Travis Hunter", school: "Colorado", pos: "WR/CB", trend: "up" },
    { id: 2, name: "Ashton Jeanty", school: "Boise State", pos: "RB", trend: "up" },
    { id: 3, name: "Tetairoa McMillan", school: "Arizona", pos: "WR", trend: "flat" },
    { id: 4, name: "Shedeur Sanders", school: "Colorado", pos: "QB", trend: "down" }, // Controversy drop
    { id: 5, name: "Luther Burden III", school: "Missouri", pos: "WR", trend: "down" },
    { id: 6, name: "Cam Ward", school: "Miami", pos: "QB", trend: "up" },
    { id: 7, name: "Emeka Egbuka", school: "Ohio State", pos: "WR", trend: "flat" },
    { id: 8, name: "Omarion Hampton", school: "UNC", pos: "RB", trend: "up" },
    { id: 9, name: "Quinshon Judkins", school: "Ohio State", pos: "RB", trend: "down" },
    { id: 10, name: "TreVeyon Henderson", school: "Ohio State", pos: "RB", trend: "flat" },
];

// ... keep CFP_MATCHUPS, BOWL_GAMES, FIRST_ROUND_ORDER ...

export const CFP_MATCHUPS = [
    { id: 1, home: "Oregon", away: "Ohio State", date: "Jan 20", time: "8:00 PM" },
    { id: 2, home: "Georgia", away: "Texas", date: "Jan 21", time: "7:30 PM" },
];

export const BOWL_GAMES = [
    { id: 1, home: "USC", away: "LSU", date: "Dec 28", time: "5:00 PM" },
    { id: 2, home: "Alabama", away: "Michigan", date: "Jan 1", time: "1:00 PM" },
    { id: 3, home: "Ole Miss", away: "Iowa", date: "Dec 30", time: "3:30 PM" },
];

// NEW: Current Projected Top 10 Order
export const FIRST_ROUND_ORDER = [
    { pick: 1, team: "New York Giants", needs: "QB" },
    { pick: 2, team: "Tennessee Titans", needs: "QB/WR" },
    { pick: 3, team: "Jacksonville Jaguars", needs: "OL/CB" },
    { pick: 4, team: "Cleveland Browns", needs: "QB/OL" },
    { pick: 5, team: "Las Vegas Raiders", needs: "QB" },
    { pick: 6, team: "New England Patriots", needs: "WR/OL" },
    { pick: 7, team: "New Orleans Saints", needs: "QB" },
    { pick: 8, team: "Carolina Panthers", needs: "WR/EDGE" },
    { pick: 9, team: "New York Jets", needs: "OL/QB" },
    { pick: 10, team: "Miami Dolphins", needs: "OL/DL" },
];

// ... keep ROOKIES_2024, PROSPECTS_2025, etc ...

// ... keep ROOKIES_2024, PROSPECTS_2025, etc ...

export const SEC_TEAMS = [
    { rank: 1, name: "Georgia", record: "12-1", havoc: "22%", ppg: "10.2", color: "#BA0C2F" },
    { rank: 2, name: "Texas", record: "11-2", havoc: "20%", ppg: "11.4", color: "#BF5700" },
    { rank: 3, name: "Alabama", record: "11-2", havoc: "19%", ppg: "13.1", color: "#9E1B32" },
    { rank: 4, name: "Ole Miss", record: "10-2", havoc: "18%", ppg: "14.5", color: "#CE1126" },
    { rank: 5, name: "Tennessee", record: "10-2", havoc: "17%", ppg: "15.2", color: "#FF8200" },
    { rank: 6, name: "LSU", record: "9-3", havoc: "16%", ppg: "17.8", color: "#461D7C" },
    { rank: 7, name: "Missouri", record: "10-2", havoc: "15%", ppg: "18.5", color: "#F1B82D" },
    { rank: 8, name: "Oklahoma", record: "10-2", havoc: "14%", ppg: "19.2", color: "#841617" },
    { rank: 9, name: "Texas A&M", record: "7-5", havoc: "14%", ppg: "21.4", color: "#500000" },
    { rank: 10, name: "Auburn", record: "6-6", havoc: "13%", ppg: "22.1", color: "#0C2340" },
    { rank: 11, name: "Kentucky", record: "7-5", havoc: "12%", ppg: "23.5", color: "#0033A0" },
    { rank: 12, name: "Florida", record: "5-7", havoc: "11%", ppg: "25.8", color: "#FA4616" },
    { rank: 13, name: "South Carolina", record: "5-7", havoc: "11%", ppg: "26.2", color: "#73000A" },
    { rank: 14, name: "Arkansas", record: "4-8", havoc: "10%", ppg: "28.4", color: "#9D2235" },
    { rank: 15, name: "Mississippi State", record: "5-7", havoc: "9%", ppg: "29.5", color: "#660000" },
    { rank: 16, name: "Vanderbilt", record: "2-10", havoc: "8%", ppg: "34.1", color: "#866D4B" },
];