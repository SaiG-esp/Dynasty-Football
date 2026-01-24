// src/data.js

// 1. IMPORT REAL DATA FROM PYTHON SCRIPT
// (Ensure this path is correct based on your folder structure)
import databaseData from './prospects.json'; 

// 2. EXPORT IT FOR THE PLAYERS DASHBOARD
export const PLAYER_DATABASE = databaseData;

// --- CONFERENCE DATA ---
export const conferenceData = [
  {
    name: "SEC",
    teams: [
      { name: "Georgia", color: "#BA0C2F", havoc: 96.5, epa: -0.28 },
      { name: "Texas", color: "#BF5700", havoc: 94.1, epa: -0.24 },
      { name: "Alabama", color: "#9E1B32", havoc: 92.3, epa: -0.21 },
      { name: "Ole Miss", color: "#14213D", havoc: 90.0, epa: -0.19 },
      { name: "Tennessee", color: "#FF8200", havoc: 88.5, epa: -0.15 },
      { name: "LSU", color: "#461D7C", havoc: 87.0, epa: -0.12 },
      { name: "Missouri", color: "#F1B82D", havoc: 85.2, epa: -0.10, darkText: true },
      { name: "Oklahoma", color: "#841617", havoc: 83.4, epa: -0.08 },
      { name: "Texas A&M", color: "#500000", havoc: 81.1, epa: -0.06 },
      { name: "Auburn", color: "#0C2340", havoc: 79.5, epa: -0.04 },
      { name: "Kentucky", color: "#0033A0", havoc: 77.0, epa: -0.02 },
      { name: "Florida", color: "#FA4616", havoc: 75.2, epa: 0.01 },
      { name: "S. Carolina", color: "#73000A", havoc: 73.0, epa: 0.03 },
      { name: "Arkansas", color: "#9D2235", havoc: 71.5, epa: 0.05 },
      { name: "Miss State", color: "#660000", havoc: 69.8, epa: 0.08 },
      { name: "Vanderbilt", color: "#866D4B", havoc: 65.0, epa: 0.12, darkText: true },
    ]
  },
  {
    name: "Big Ten",
    teams: [
      { name: "Ohio State", color: "#BB0000", havoc: 94.2, epa: -0.22 },
      { name: "Michigan", color: "#00274C", havoc: 91.5, epa: -0.19 },
      { name: "Oregon", color: "#154733", havoc: 89.8, epa: -0.15 },
      { name: "Penn State", color: "#041E42", havoc: 88.4, epa: -0.14 },
      { name: "Iowa", color: "#FFCD00", havoc: 87.1, epa: -0.18, darkText: true },
      { name: "Wisconsin", color: "#C5050C", havoc: 85.5, epa: -0.11 },
      { name: "USC", color: "#990000", havoc: 84.0, epa: -0.09 },
      { name: "Washington", color: "#4B2E83", havoc: 82.3, epa: -0.08 },
      { name: "UCLA", color: "#2D68C4", havoc: 80.5, epa: -0.07 },
      { name: "Nebraska", color: "#E41C38", havoc: 78.9, epa: -0.05 },
      { name: "Michigan St", color: "#18453B", havoc: 77.2, epa: -0.04 },
      { name: "Minnesota", color: "#7A0019", havoc: 76.5, epa: -0.03 },
      { name: "Maryland", color: "#E03A3E", havoc: 75.1, epa: -0.02 },
      { name: "Illinois", color: "#E84A27", havoc: 74.0, epa: -0.01 },
      { name: "Rutgers", color: "#D21034", havoc: 72.5, epa: 0.02 },
      { name: "Purdue", color: "#CEB888", havoc: 70.8, epa: 0.05, darkText: true },
      { name: "Northwestern", color: "#4E2A84", havoc: 69.4, epa: 0.08 },
      { name: "Indiana", color: "#990000", havoc: 68.0, epa: 0.10 },
    ]
  },
  {
    name: "ACC",
    teams: [
      { name: "Miami", color: "#F47321", havoc: 93.5, epa: -0.25 },
      { name: "Clemson", color: "#F56600", havoc: 91.0, epa: -0.22 },
      { name: "SMU", color: "#354CA1", havoc: 89.2, epa: -0.18 },
      { name: "Florida St", color: "#782F40", havoc: 87.5, epa: -0.15 },
      { name: "Louisville", color: "#C9001F", havoc: 85.0, epa: -0.11 },
      { name: "NC State", color: "#CC0000", havoc: 83.5, epa: -0.09 },
      { name: "N. Carolina", color: "#7BAFD4", havoc: 82.0, epa: -0.07, darkText: true },
      { name: "Va Tech", color: "#630031", havoc: 80.2, epa: -0.05 },
      { name: "Duke", color: "#003087", havoc: 79.0, epa: -0.04 },
      { name: "Pittsburgh", color: "#003594", havoc: 77.5, epa: -0.03 },
      { name: "California", color: "#003262", havoc: 76.1, epa: -0.02 },
      { name: "Ga Tech", color: "#B3A369", havoc: 74.8, epa: 0.01, darkText: true },
      { name: "Syracuse", color: "#D44500", havoc: 73.2, epa: 0.03 },
      { name: "Wake Forest", color: "#9E7E38", havoc: 71.5, epa: 0.06, darkText: true },
      { name: "Virginia", color: "#232D4B", havoc: 70.0, epa: 0.09 },
      { name: "Boston Col", color: "#98002E", havoc: 68.5, epa: 0.12 },
      { name: "Stanford", color: "#8C1515", havoc: 66.2, epa: 0.15 },
    ]
  },
  {
    name: "Big 12",
    teams: [
      { name: "Utah", color: "#CC0000", havoc: 92.1, epa: -0.20 },
      { name: "Kansas St", color: "#512888", havoc: 90.5, epa: -0.18 },
      { name: "Oklahoma St", color: "#FF7300", havoc: 88.2, epa: -0.15 },
      { name: "Iowa State", color: "#C8102E", havoc: 87.0, epa: -0.12 },
      { name: "Arizona", color: "#CC0033", havoc: 85.5, epa: -0.10 },
      { name: "West Virginia", color: "#002855", havoc: 84.1, epa: -0.09 },
      { name: "Texas Tech", color: "#CC0000", havoc: 82.8, epa: -0.08 },
      { name: "Kansas", color: "#0051BA", havoc: 81.0, epa: -0.06 },
      { name: "BYU", color: "#002E62", havoc: 80.5, epa: -0.05 },
      { name: "UCF", color: "#BA9B37", havoc: 79.5, epa: -0.05, darkText: true },
      { name: "TCU", color: "#4D1979", havoc: 78.0, epa: -0.04 },
      { name: "Colorado", color: "#000000", havoc: 77.2, epa: -0.03 },
      { name: "Baylor", color: "#154734", havoc: 76.5, epa: -0.02 },
      { name: "Cincinnati", color: "#E00122", havoc: 73.5, epa: 0.01 },
      { name: "Houston", color: "#C8102E", havoc: 71.2, epa: 0.04 },
      { name: "Arizona St", color: "#8C1D40", havoc: 69.8, epa: 0.07 },
    ]
  },
  {
    name: "American",
    teams: [
      { name: "Navy", color: "#00205B", havoc: 88.0, epa: -0.15 },
      { name: "Tulane", color: "#006747", havoc: 86.5, epa: -0.12 },
      { name: "Army", color: "#D4BF80", havoc: 84.0, epa: -0.08, darkText: true },
      { name: "Memphis", color: "#003087", havoc: 83.2, epa: -0.07 },
      { name: "UTSA", color: "#F15A22", havoc: 81.5, epa: -0.06 },
      { name: "S. Florida", color: "#006747", havoc: 79.8, epa: -0.04 },
      { name: "E. Carolina", color: "#592A8A", havoc: 78.5, epa: -0.03 },
      { name: "Fla Atlantic", color: "#003366", havoc: 77.0, epa: -0.02 },
      { name: "Rice", color: "#00205B", havoc: 76.2, epa: 0.01 },
      { name: "UAB", color: "#006341", havoc: 75.0, epa: 0.02 },
      { name: "North Texas", color: "#00853E", havoc: 74.1, epa: 0.04 },
      { name: "Tulsa", color: "#002D72", havoc: 72.8, epa: 0.06 },
      { name: "Charlotte", color: "#00703C", havoc: 71.5, epa: 0.08 },
      { name: "Temple", color: "#9D2235", havoc: 69.5, epa: 0.10 },
    ]
  },
  {
    name: "Mountain West",
    teams: [
      { name: "Boise State", color: "#0033A0", havoc: 85.5, epa: -0.16 },
      { name: "UNLV", color: "#CF0A2C", havoc: 83.0, epa: -0.13 },
      { name: "Fresno State", color: "#C41230", havoc: 81.2, epa: -0.10 },
      { name: "Air Force", color: "#003087", havoc: 79.8, epa: -0.08 },
      { name: "Wyoming", color: "#FFC425", havoc: 78.0, epa: -0.06, darkText: true },
      { name: "San Jose St", color: "#0055A2", havoc: 76.5, epa: -0.04 },
      { name: "Colorado St", color: "#1E4D2B", havoc: 75.0, epa: -0.02 },
      { name: "San Diego St", color: "#A6192E", havoc: 73.8, epa: 0.01 },
      { name: "Utah State", color: "#0F2439", havoc: 72.0, epa: 0.04 },
      { name: "Hawaii", color: "#024731", havoc: 70.5, epa: 0.06 },
      { name: "New Mexico", color: "#CE0037", havoc: 68.2, epa: 0.09 },
      { name: "Nevada", color: "#002E62", havoc: 66.5, epa: 0.12 },
    ]
  },
  {
    name: "MAC",
    teams: [
      { name: "W. Michigan", color: "#532E1F", havoc: 82.5, epa: -0.14 },
      { name: "Toledo", color: "#003E7E", havoc: 81.0, epa: -0.12 },
      { name: "Miami (OH)", color: "#B61E2E", havoc: 79.5, epa: -0.09 },
      { name: "Ohio", color: "#00694E", havoc: 78.2, epa: -0.07 },
      { name: "Bowling Green", color: "#FE5000", havoc: 76.5, epa: -0.05, darkText: true },
      { name: "N. Illinois", color: "#BA0C2F", havoc: 75.0, epa: -0.03 },
      { name: "Buffalo", color: "#005BBB", havoc: 73.8, epa: -0.01 },
      { name: "C. Michigan", color: "#6A0032", havoc: 72.0, epa: 0.01 },
      { name: "E. Michigan", color: "#006533", havoc: 70.5, epa: 0.03 },
      { name: "Ball State", color: "#BA0C2F", havoc: 68.2, epa: 0.05 },
      { name: "Akron", color: "#041E42", havoc: 67.0, epa: 0.08 },
      { name: "Kent State", color: "#00244E", havoc: 65.5, epa: 0.11 },
      { name: "UMass", color: "#881C1C", havoc: 64.0, epa: 0.13 },
    ]
  },
  {
    name: "Independents",
    teams: [
      { name: "Notre Dame", color: "#C99700", havoc: 89.5, epa: -0.17, darkText: true },
      { name: "Liberty", color: "#0A254E", havoc: 86.2, epa: -0.12 },
      { name: "UConn", color: "#000E2F", havoc: 76.0, epa: 0.02 },
    ]
  }
];
 
// --- AP POLL DATA ---
export const apTop25Data = [
  { rank: 1, name: "Oregon", record: "12-0" },
  { rank: 2, name: "Ohio State", record: "11-1" },
  { rank: 3, name: "Texas", record: "11-1" },
  { rank: 4, name: "Penn State", record: "11-1" },
  { rank: 5, name: "Notre Dame", record: "11-1" },
  { rank: 6, name: "Georgia", record: "10-2" },
  { rank: 7, name: "Tennessee", record: "10-2" },
  { rank: 8, name: "SMU", record: "11-1" },
  { rank: 9, name: "Indiana", record: "11-1" },
  { rank: 10, name: "Boise State", record: "11-1" },
  { rank: 11, name: "Alabama", record: "9-3" },
  { rank: 12, name: "Miami", record: "10-2" },
  { rank: 13, name: "Ole Miss", record: "10-2" },
  { rank: 14, name: "Arizona State", record: "10-2" },
  { rank: 15, name: "BYU", record: "10-2" },
  { rank: 16, name: "Iowa State", record: "10-2" },
  { rank: 17, name: "Clemson", record: "9-3" },
  { rank: 18, name: "South Carolina", record: "9-3" },
  { rank: 19, name: "Army", record: "10-1" },
  { rank: 20, name: "Tulane", record: "10-2" },
  { rank: 21, name: "UNLV", record: "10-2" },
  { rank: 22, name: "Illinois", record: "9-3" },
  { rank: 23, name: "Missouri", record: "9-3" },
  { rank: 24, name: "Colorado", record: "9-3" },
  { rank: 25, name: "Memphis", record: "10-2" },
];
 
// --- HOME PAGE DATA ---
export const CFP_MATCHUPS = [
  { id: 1, home: "Oregon", away: "Ohio State", date: "Jan 20" },
  { id: 2, home: "Georgia", away: "Texas", date: "Jan 21" }
];
 
export const BOWL_GAMES = [
  { id: 1, home: "USC", away: "LSU", date: "Dec 28" },
  { id: 2, home: "Alabama", away: "Michigan", date: "Jan 1" },
  { id: 3, home: "Ole Miss", away: "Iowa", date: "Dec 30" }
];
 
// --- EXPANDED DATA FOR HOME PAGE ---
// UPDATED ORDER BASED ON YOUR LIST
export const FIRST_ROUND_ORDER = [
  { pick: 1, team: "Las Vegas Raiders", needs: "QB" },
  { pick: 2, team: "New York Jets", needs: "QB/OL" },
  { pick: 3, team: "Arizona Cardinals", needs: "DL/EDGE" },
  { pick: 4, team: "Tennessee Titans", needs: "QB/WR" },
  { pick: 5, team: "New York Giants", needs: "QB/OL" },
  { pick: 6, team: "Cleveland Browns", needs: "OT/WR" },
  { pick: 7, team: "Washington Commanders", needs: "CB/OT" },
  { pick: 8, team: "New Orleans Saints", needs: "QB/WR" },
  { pick: 9, team: "Kansas City Chiefs", needs: "WR/CB" },
  { pick: 10, team: "Cincinnati Bengals", needs: "DL/OL" },
  { pick: 11, team: "Miami Dolphins", needs: "OL/DL" },
  { pick: 12, team: "Dallas Cowboys", needs: "RB/DT" },
  { pick: 13, team: "Los Angeles Rams", needs: "CB/OT" },
  { pick: 14, team: "Baltimore Ravens", needs: "OL/EDGE" },
  { pick: 15, team: "Tampa Bay Bucs", needs: "EDGE" },
  { pick: 16, team: "New York Jets", needs: "Best Avail" }, 
  { pick: 17, team: "Detroit Lions", needs: "EDGE/OL" },
  { pick: 18, team: "Minnesota Vikings", needs: "CB/DT" }
];
 
// --- BIG BOARD / CURATED PROSPECTS ---
// SEND ME YOUR NEW LIST TO UPDATE THIS!
// --- BIG BOARD / CURATED PROSPECTS ---
export const PROSPECTS_2025 = [
  { id: 1, name: "Jeremiyah Love", school: "Notre Dame", pos: "RB", trend: "up" },
  { id: 2, name: "Makai Lemon", school: "USC", pos: "WR", trend: "up" },
  { id: 3, name: "Jordyn Tyson", school: "Arizona State", pos: "WR", trend: "up" },
  { id: 4, name: "Denzel Boston", school: "Washington", pos: "WR", trend: "flat" },
  { id: 5, name: "Jadarian Price", school: "Notre Dame", pos: "RB", trend: "flat" },
  { id: 6, name: "Jonah Coleman", school: "Washington", pos: "RB", trend: "up" },
  { id: 7, name: "Kenyon Sadiq", school: "Oregon", pos: "TE", trend: "flat" },
  { id: 8, name: "Carnell Tate", school: "Ohio State", pos: "WR", trend: "flat" },
  { id: 9, name: "KC Concepcion", school: "Texas A&M", pos: "WR", trend: "down" }, // Transferred from NC State
  { id: 10, name: "Justice Haynes", school: "Michigan", pos: "RB", trend: "up" }, // Transferred from Alabama
  { id: 11, name: "Chris Bell", school: "Louisville", pos: "WR", trend: "flat" },
  { id: 12, name: "Nicholas Singleton", school: "Penn State", pos: "RB", trend: "down" },
  { id: 13, name: "Emmett Johnson", school: "Nebraska", pos: "RB", trend: "up" },
  { id: 14, name: "Germie Bernard", school: "Alabama", pos: "WR", trend: "flat" },
  { id: 15, name: "Fernando Mendoza", school: "Indiana", pos: "QB", trend: "up" },
  { id: 16, name: "Dante Moore", school: "Oregon", pos: "QB", trend: "flat" },
  { id: 17, name: "Elijah Sarratt", school: "Indiana", pos: "WR", trend: "up" },
  { id: 18, name: "Kaytron Allen", school: "Penn State", pos: "RB", trend: "flat" },
  { id: 19, name: "Ja'Kobi Lane", school: "USC", pos: "WR", trend: "up" },
  { id: 20, name: "Chris Brazzell II", school: "Tennessee", pos: "WR", trend: "flat" },
  { id: 21, name: "LJ Martin", school: "BYU", pos: "RB", trend: "down" },
  { id: 22, name: "Eli Stowers", school: "Vanderbilt", pos: "TE", trend: "up" },
  { id: 23, name: "Antonio Williams", school: "Clemson", pos: "WR", trend: "flat" },
  { id: 24, name: "Michael Trigg", school: "Baylor", pos: "TE", trend: "down" }
];
 
// --- PLAYER ARCHETYPE DATA ---
export const samplePlayers = {
  1: {
    id: 1,
    name: "Shedeur Sanders",
    school: "Colorado",
    position: "QB",
    number: "#2",
    height: "6'2\"",
    weight: "215 lbs",
    class: "Senior",
    stats: {
      passingYards: "3,230",
      tds: "27",
      ints: "3",
      completion: "69.3%",
      epa: "+0.33",
      havocAvoided: "92%"
    },
    scoutingReport: "Elite pocket presence with surgical accuracy. Displays calmness under pressure that translates well to the next level."
  },
  2: {
    id: 2,
    name: "Travis Hunter",
    school: "Colorado",
    position: "WR/CB",
    number: "#12",
    height: "6'1\"",
    weight: "185 lbs",
    class: "Junior",
    stats: {
      receptions: "74",
      yards: "911",
      tds: "9",
      interceptions: "3",
      epa: "+0.45",
      havocCreated: "Elite"
    },
    scoutingReport: "Generational dual-threat talent. Fluid hips at CB and explosive route running at WR. A true game-changer."
  }
};