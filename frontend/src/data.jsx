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
      { name: "Oklahoma", color: "#841617", havoc: 98.1, epa: 0.0 },
      { name: "Missouri", color: "#F1B82D", havoc: 94.4, epa: 0.04, darkText: true },
      { name: "Auburn", color: "#0C2340", havoc: 61.1, epa: 0.07 },
      { name: "Alabama", color: "#9E1B32", havoc: 79.6, epa: 0.08 },
      { name: "LSU", color: "#461D7C", havoc: 68.5, epa: 0.08 },
      { name: "S. Carolina", color: "#73000A", havoc: 54.6, epa: 0.09 },
      { name: "Texas", color: "#BF5700", havoc: 81.5, epa: 0.1 },
      { name: "Georgia", color: "#BA0C2F", havoc: 44.4, epa: 0.1 },
      { name: "Texas A&M", color: "#500000", havoc: 97.2, epa: 0.13 },
      { name: "Ole Miss", color: "#14213D", havoc: 64.8, epa: 0.13 },
      { name: "Tennessee", color: "#FF8200", havoc: 86.1, epa: 0.16 },
      { name: "Kentucky", color: "#0033A0", havoc: 34.3, epa: 0.18 },
      { name: "Florida", color: "#FA4616", havoc: 30.6, epa: 0.18 },
      { name: "Vanderbilt", color: "#866D4B", havoc: 69.4, epa: 0.2 },
      { name: "Miss State", color: "#660000", havoc: 22.2, epa: 0.22 },
      { name: "Arkansas", color: "#9D2235", havoc: 49.1, epa: 0.27 },
    ]
  },
  {
    name: "Big Ten",
    teams: [
      { name: "Ohio State", color: "#BB0000", havoc: 57.4, epa: -0.02 },
      { name: "Indiana", color: "#990000", havoc: 99.1, epa: 0.03 },
      { name: "Oregon", color: "#154733", havoc: 84.3, epa: 0.05 },
      { name: "Iowa", color: "#FFCD00", havoc: 67.6, epa: 0.08, darkText: true },
      { name: "Washington", color: "#4B2E83", havoc: 33.3, epa: 0.08 },
      { name: "Michigan", color: "#00274C", havoc: 64.8, epa: 0.12 },
      { name: "Penn State", color: "#041E42", havoc: 52.8, epa: 0.12 },
      { name: "Maryland", color: "#E03A3E", havoc: 27.8, epa: 0.13 },
      { name: "USC", color: "#990000", havoc: 52.8, epa: 0.16 },
      { name: "Northwestern", color: "#4E2A84", havoc: 41.7, epa: 0.17 },
      { name: "Wisconsin", color: "#C5050C", havoc: 14.8, epa: 0.19 },
      { name: "Minnesota", color: "#7A0019", havoc: 76.9, epa: 0.2 },
      { name: "Illinois", color: "#E84A27", havoc: 48.1, epa: 0.2 },
      { name: "Nebraska", color: "#E41C38", havoc: 29.6, epa: 0.21 },
      { name: "Michigan St", color: "#18453B", havoc: 22.2, epa: 0.21 },
      { name: "UCLA", color: "#2D68C4", havoc: 6.5, epa: 0.25 },
      { name: "Purdue", color: "#CEB888", havoc: 46.3, epa: 0.27, darkText: true },
      { name: "Rutgers", color: "#D21034", havoc: 11.1, epa: 0.31 },
    ]
  },
  {
    name: "ACC",
    teams: [
      { name: "SMU", color: "#354CA1", havoc: 88.9, epa: 0.03 },
      { name: "Wake Forest", color: "#9E7E38", havoc: 84.3, epa: 0.03 },
      { name: "Miami", color: "#F47321", havoc: 90.7, epa: 0.05 },
      { name: "Louisville", color: "#C9001F", havoc: 74.1, epa: 0.05 },
      { name: "Virginia", color: "#232D4B", havoc: 82.4, epa: 0.06 },
      { name: "Pittsburgh", color: "#003594", havoc: 90.7, epa: 0.08 },
      { name: "Clemson", color: "#F56600", havoc: 93.5, epa: 0.11 },
      { name: "Florida St", color: "#782F40", havoc: 50.0, epa: 0.16 },
      { name: "California", color: "#003262", havoc: 44.4, epa: 0.17 },
      { name: "Stanford", color: "#8C1515", havoc: 33.3, epa: 0.17 },
      { name: "N. Carolina", color: "#7BAFD4", havoc: 36.1, epa: 0.18, darkText: true },
      { name: "Ga Tech", color: "#B3A369", havoc: 24.1, epa: 0.2, darkText: true },
      { name: "NC State", color: "#CC0000", havoc: 40.7, epa: 0.21 },
      { name: "Duke", color: "#003087", havoc: 71.3, epa: 0.23 },
      { name: "Boston Col", color: "#98002E", havoc: 10.2, epa: 0.23 },
      { name: "Syracuse", color: "#D44500", havoc: 19.4, epa: 0.28 },
      { name: "Va Tech", color: "#630031", havoc: 17.6, epa: 0.28 },
    ]
  },
  {
    name: "Big 12",
    teams: [
      { name: "Texas Tech", color: "#CC0000", havoc: 100.0, epa: -0.09 },
      { name: "Utah", color: "#CC0000", havoc: 67.6, epa: 0.07 },
      { name: "Iowa State", color: "#C8102E", havoc: 64.8, epa: 0.09 },
      { name: "BYU", color: "#002E62", havoc: 50.9, epa: 0.09 },
      { name: "Arizona", color: "#CC0033", havoc: 96.3, epa: 0.1 },
      { name: "Arizona St", color: "#8C1D40", havoc: 88.9, epa: 0.1 },
      { name: "Houston", color: "#C8102E", havoc: 56.5, epa: 0.11 },
      { name: "UCF", color: "#BA9B37", havoc: 58.3, epa: 0.12 },
      { name: "Kansas St", color: "#512888", havoc: 64.8, epa: 0.13 },
      { name: "TCU", color: "#4D1979", havoc: 40.7, epa: 0.15 },
      { name: "West Virginia", color: "#002855", havoc: 79.6, epa: 0.16 },
      { name: "Baylor", color: "#154734", havoc: 10.2, epa: 0.18 },
      { name: "Colorado", color: "#000000", havoc: 44.4, epa: 0.21 },
      { name: "Cincinnati", color: "#E00122", havoc: 8.3, epa: 0.21 },
      { name: "Kansas", color: "#0051BA", havoc: 79.6, epa: 0.25 },
      { name: "Oklahoma St", color: "#FF7300", havoc: 40.7, epa: 0.28 },
    ]
  },
  {
    name: "American",
    teams: [
      { name: "S. Florida", color: "#006747", havoc: 55.6, epa: 0.07 },
      { name: "E. Carolina", color: "#592A8A", havoc: 92.6, epa: 0.09 },
      { name: "Tulane", color: "#006747", havoc: 59.3, epa: 0.15 },
      { name: "Tulsa", color: "#002D72", havoc: 13.9, epa: 0.15 },
      { name: "UTSA", color: "#F15A22", havoc: 87.0, epa: 0.18 },
      { name: "North Texas", color: "#00853E", havoc: 24.1, epa: 0.18 },
      { name: "Army", color: "#D4BF80", havoc: 13.9, epa: 0.18, darkText: true },
      { name: "Memphis", color: "#003087", havoc: 75.9, epa: 0.19 },
      { name: "Navy", color: "#00205B", havoc: 12.0, epa: 0.21 },
      { name: "Rice", color: "#00205B", havoc: 22.2, epa: 0.25 },
      { name: "Fla Atlantic", color: "#003366", havoc: 25.9, epa: 0.26 },
      { name: "Charlotte", color: "#00703C", havoc: 2.8, epa: 0.26 },
      { name: "Temple", color: "#9D2235", havoc: 33.3, epa: 0.28 },
      { name: "UAB", color: "#006341", havoc: 6.5, epa: 0.34 },
    ]
  },
  {
    name: "Mountain West",
    teams: [
      { name: "San Diego St", color: "#A6192E", havoc: 46.3, epa: -0.01 },
      { name: "Wyoming", color: "#FFC425", havoc: 15.7, epa: 0.07, darkText: true },
      { name: "Fresno State", color: "#C41230", havoc: 75.9, epa: 0.11 },
      { name: "New Mexico", color: "#CE0037", havoc: 71.3, epa: 0.11 },
      { name: "Boise State", color: "#0033A0", havoc: 61.1, epa: 0.12 },
      { name: "Hawaii", color: "#024731", havoc: 54.6, epa: 0.17 },
      { name: "Nevada", color: "#002E62", havoc: 29.6, epa: 0.19 },
      { name: "San Jose St", color: "#005893", havoc: 7.4, epa: 0.2 },
      { name: "UNLV", color: "#CF0A2C", havoc: 40.7, epa: 0.21 },
      { name: "Utah State", color: "#0F2439", havoc: 19.4, epa: 0.22 },
      { name: "Colorado St", color: "#1E4D2B", havoc: 17.6, epa: 0.24 },
      { name: "Air Force", color: "#003087", havoc: 3.7, epa: 0.41 },
    ]
  },
  {
    name: "MAC",
    teams: [
      { name: "Toledo", color: "#003E7E", havoc: 96.3, epa: -0.07 },
      { name: "W. Michigan", color: "#532E1F", havoc: 74.1, epa: 0.06 },
      { name: "Miami (OH)", color: "#B61E2E", havoc: 80.6, epa: 0.08 },
      { name: "C. Michigan", color: "#6A0032", havoc: 67.6, epa: 0.1 },
      { name: "Akron", color: "#041E42", havoc: 74.1, epa: 0.11 },
      { name: "Buffalo", color: "#005BBB", havoc: 48.1, epa: 0.12 },
      { name: "Ohio", color: "#00694E", havoc: 40.7, epa: 0.12 },
      { name: "Bowling Green", color: "#FE5000", havoc: 91.7, epa: 0.15 },
      { name: "Ball State", color: "#BA0C2F", havoc: 26.9, epa: 0.18 },
      { name: "Kent State", color: "#00244E", havoc: 25.0, epa: 0.19 },
      { name: "N. Illinois", color: "#BA0C2F", havoc: 4.6, epa: 0.19 },
      { name: "E. Michigan", color: "#006533", havoc: 2.8, epa: 0.24 },
      { name: "UMass", color: "#881C1C", havoc: 0.9, epa: 0.28 },
    ]
  },
  {
    name: "Independents",
    teams: [
      { name: "Notre Dame", color: "#C99700", havoc: 86.1, epa: 0.04 },
      { name: "UConn", color: "#000E2F", havoc: 36.1, epa: 0.22 },
    ]
  },
];
 
// --- AP POLL DATA (Final 2025 season / 2026 CFP cycle) ---
export const apTop25Data = [
  { rank: 1, name: "Indiana", record: "16-0" },
  { rank: 2, name: "Miami", record: "14-3" },
  { rank: 3, name: "Ole Miss", record: "13-2" },
  { rank: 4, name: "Oregon", record: "13-2" },
  { rank: 5, name: "Ohio State", record: "12-2" },
  { rank: 6, name: "Georgia", record: "12-2" },
  { rank: 7, name: "Texas Tech", record: "12-2" },
  { rank: 8, name: "Texas A&M", record: "11-2" },
  { rank: 9, name: "Alabama", record: "11-3" },
  { rank: 10, name: "Notre Dame", record: "10-2" },
  { rank: 11, name: "BYU", record: "12-2" },
  { rank: 12, name: "Texas", record: "10-3" },
  { rank: 13, name: "Oklahoma", record: "10-3" },
  { rank: 14, name: "Utah", record: "11-2" },
  { rank: 15, name: "Vanderbilt", record: "10-3" },
  { rank: 16, name: "Virginia", record: "11-3" },
  { rank: 17, name: "Iowa", record: "9-4" },
  { rank: 18, name: "Tulane", record: "11-3" },
  { rank: 19, name: "James Madison", record: "12-2" },
  { rank: 20, name: "USC", record: "9-4" },
  { rank: 21, name: "Michigan", record: "9-4" },
  { rank: 22, name: "Houston", record: "10-3" },
  { rank: 23, name: "Navy", record: "10-2" },
  { rank: 24, name: "North Texas", record: "11-2" },
  { rank: 25, name: "TCU", record: "9-4" },
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
// 2026 NFL Draft — Round 1 results
export const FIRST_ROUND_ORDER = [
  { pick: 1, team: "Las Vegas Raiders", needs: "QB · Mendoza" },
  { pick: 2, team: "New York Jets", needs: "EDGE · Bailey" },
  { pick: 3, team: "Arizona Cardinals", needs: "RB · Love" },
  { pick: 4, team: "Tennessee Titans", needs: "WR · Tate" },
  { pick: 5, team: "New York Giants", needs: "EDGE · Reese" },
  { pick: 6, team: "Kansas City Chiefs", needs: "CB · Delane" },
  { pick: 7, team: "Washington Commanders", needs: "LB · Styles" },
  { pick: 8, team: "New Orleans Saints", needs: "WR · Tyson" },
  { pick: 9, team: "Cleveland Browns", needs: "OT · Fano" },
  { pick: 10, team: "New York Giants", needs: "OT · Mauigoa" },
  { pick: 11, team: "Dallas Cowboys", needs: "S · Downs" },
  { pick: 12, team: "Miami Dolphins", needs: "OT · Proctor" },
  { pick: 13, team: "Los Angeles Rams", needs: "QB · Simpson" },
  { pick: 14, team: "Baltimore Ravens", needs: "G · Ioane" },
  { pick: 15, team: "Tampa Bay Bucs", needs: "EDGE · Bain" },
  { pick: 16, team: "New York Jets", needs: "TE · Sadiq" },
  { pick: 17, team: "Detroit Lions", needs: "OT · Miller" },
  { pick: 18, team: "Minnesota Vikings", needs: "DT · Banks" },
  { pick: 19, team: "Carolina Panthers", needs: "OT · Freeling" },
  { pick: 20, team: "Philadelphia Eagles", needs: "WR · Lemon" },
  { pick: 21, team: "Pittsburgh Steelers", needs: "OT · Iheanachor" },
  { pick: 22, team: "Los Angeles Chargers", needs: "EDGE · Mesidor" },
  { pick: 23, team: "Dallas Cowboys", needs: "EDGE · Lawrence" },
  { pick: 24, team: "Cleveland Browns", needs: "WR · Concepcion" },
  { pick: 25, team: "Chicago Bears", needs: "S · Thieneman" },
  { pick: 26, team: "Houston Texans", needs: "G · Rutledge" },
  { pick: 27, team: "Miami Dolphins", needs: "CB · Johnson" },
  { pick: 28, team: "New England Patriots", needs: "OT · Lomu" },
  { pick: 29, team: "Kansas City Chiefs", needs: "DT · Woods" },
  { pick: 30, team: "New York Jets", needs: "WR · Cooper" },
  { pick: 31, team: "Tennessee Titans", needs: "EDGE · Faulk" },
  { pick: 32, team: "Seattle Seahawks", needs: "RB · Price" }
];

// --- BIG BOARD / CURATED PROSPECTS ---
// Offensive skill-position board for the 2026 NFL Draft class
export const PROSPECTS_2026 = [
  { id: 4837248, name: "Fernando Mendoza", school: "Indiana", pos: "QB", trend: "up" },
  { id: 4870808, name: "Jeremiyah Love", school: "Notre Dame", pos: "RB", trend: "up" },
  { id: 4871023, name: "Carnell Tate", school: "Ohio State", pos: "WR", trend: "up" },
  { id: 4880281, name: "Jordyn Tyson", school: "Arizona State", pos: "WR", trend: "up" },
  { id: 4870795, name: "Makai Lemon", school: "USC", pos: "WR", trend: "up" },
  { id: 5083315, name: "Kenyon Sadiq", school: "Oregon", pos: "TE", trend: "flat" },
  { id: 4685522, name: "Ty Simpson", school: "Alabama", pos: "QB", trend: "up" },
  { id: 4723820, name: "Omar Cooper Jr.", school: "Indiana", pos: "WR", trend: "up" },
  { id: 4870653, name: "KC Concepcion", school: "Texas A&M", pos: "WR", trend: "flat" },
  { id: 4685512, name: "Jadarian Price", school: "Notre Dame", pos: "RB", trend: "flat" },
  { id: 4832800, name: "Denzel Boston", school: "Washington", pos: "WR", trend: "flat" },
  { id: 4702555, name: "Jonah Coleman", school: "Washington", pos: "RB", trend: "up" },
  { id: 4869961, name: "Chris Bell", school: "Louisville", pos: "WR", trend: "flat" },
  { id: 4685261, name: "Germie Bernard", school: "Alabama", pos: "WR", trend: "flat" },
  { id: 5091739, name: "Chris Brazzell II", school: "Tennessee", pos: "WR", trend: "flat" },
  { id: 5088338, name: "Elijah Sarratt", school: "Indiana", pos: "WR", trend: "up" },
  { id: 4431574, name: "Eli Stowers", school: "Vanderbilt", pos: "TE", trend: "up" },
  { id: 4832955, name: "Emmett Johnson", school: "Nebraska", pos: "RB", trend: "up" },
  { id: 4685246, name: "Kaytron Allen", school: "Penn State", pos: "RB", trend: "flat" },
  { id: 5081432, name: "Antonio Williams", school: "Clemson", pos: "WR", trend: "flat" },
  { id: 4594749, name: "Michael Trigg", school: "Baylor", pos: "TE", trend: "down" },
  { id: 4870760, name: "Justice Haynes", school: "Michigan", pos: "RB", trend: "up" },
  { id: 4918126, name: "LJ Martin", school: "BYU", pos: "RB", trend: "down" },
  { id: 4870847, name: "Ja'Kobi Lane", school: "USC", pos: "WR", trend: "up" }
];

// Back-compat alias for any lingering imports
export const PROSPECTS_2025 = PROSPECTS_2026;
 
// --- PLAYER ARCHETYPE DATA ---
export const samplePlayers = {
  4837248: {
    id: 4837248,
    name: "Fernando Mendoza",
    school: "Indiana",
    position: "QB",
    number: "#15",
    height: "6'5\"",
    weight: "225 lbs",
    class: "Junior",
    stats: {
      passingYards: "3,811",
      tds: "48",
      ints: "6",
      completion: "71.2%",
      epa: "+0.41",
      havocAvoided: "94%"
    },
    scoutingReport: "Heisman-winning pocket passer who led Indiana to a perfect national title season. Elite processing, anticipation, and toughness under pressure."
  },
  4870808: {
    id: 4870808,
    name: "Jeremiyah Love",
    school: "Notre Dame",
    position: "RB",
    number: "#4",
    height: "6'0\"",
    weight: "214 lbs",
    class: "Junior",
    stats: {
      rushingYards: "1,652",
      tds: "21",
      receptions: "27",
      ypc: "6.1",
      epa: "+0.38",
      havocCreated: "Elite"
    },
    scoutingReport: "Prototype every-down back with home-run speed and receiving polish. The clear RB1 of the 2026 class and a top-three overall talent."
  }
};
