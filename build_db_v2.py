"""
North American City Bigness Index v2
60 cities — rebuilt from Chris's curated data
Skyline: his Excel sheet (6mo vintage, topped-out counts)
Airports: his Excel sheet
Sports: his Excel sheet
Metro pop ranks: his sheet
Phase 2 metrics: transit, conventions, landmarks, HQs (estimated)

Notes preserved verbatim where provided.
"Victor Wembanyama doesn't count as a hi-rise" — Chris, 2024
"""

import sqlite3, os

DB_PATH = "city_bigness_v2.db"

def build():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE cities (
        city_id      INTEGER PRIMARY KEY,
        name         TEXT NOT NULL,
        country      TEXT NOT NULL,
        metro_pop_rank INTEGER,
        notes        TEXT
    );

    -- Skyline: cumulative counts (e.g. 150m+ means ALL buildings above 150m)
    -- matching Chris's sheet format exactly
    CREATE TABLE skyline_data (
        city_id      INTEGER PRIMARY KEY REFERENCES cities(city_id),
        over_100m    INTEGER DEFAULT 0,
        over_150m    INTEGER DEFAULT 0,
        over_200m    INTEGER DEFAULT 0,
        over_250m    INTEGER DEFAULT 0,
        over_300m    INTEGER DEFAULT 0,
        over_350m    INTEGER DEFAULT 0,
        over_400m    INTEGER DEFAULT 0,
        skyline_rank INTEGER,
        notes        TEXT
    );

    CREATE TABLE airports (
        city_id        INTEGER PRIMARY KEY REFERENCES cities(city_id),
        total_pax_millions REAL,
        airport_count  INTEGER,
        iata_codes     TEXT,
        airport_rank   INTEGER,
        notes          TEXT
    );

    -- Sports: exact counts from Chris's sheet
    CREATE TABLE sports_teams (
        city_id        INTEGER PRIMARY KEY REFERENCES cities(city_id),
        nfl            INTEGER DEFAULT 0,
        nba            INTEGER DEFAULT 0,
        mlb            INTEGER DEFAULT 0,
        nhl            INTEGER DEFAULT 0,
        big4_total     INTEGER DEFAULT 0,
        sports_rank    INTEGER,
        notes          TEXT
    );

    -- Phase 2 metrics
    CREATE TABLE transit_systems (
        city_id        INTEGER PRIMARY KEY REFERENCES cities(city_id),
        system_name    TEXT,
        annual_riders  INTEGER DEFAULT 0
    );

    CREATE TABLE convention_centers (
        city_id        INTEGER PRIMARY KEY REFERENCES cities(city_id),
        venue_name     TEXT,
        sqft           INTEGER DEFAULT 0
    );

    CREATE TABLE landmarks (
        landmark_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id        INTEGER REFERENCES cities(city_id),
        name           TEXT,
        tier           INTEGER,
        natural        INTEGER DEFAULT 0
    );

    CREATE TABLE corporate_hq (
        city_id        INTEGER PRIMARY KEY REFERENCES cities(city_id),
        f500_count     INTEGER DEFAULT 0,
        notes          TEXT
    );
    """)

    # ─────────────────────────────────────────────────────────────
    # CITIES — 60 entries, metro_pop_rank from Chris's sheet
    # ─────────────────────────────────────────────────────────────
    cities = [
        # id, name, country, metro_pop_rank, notes
        (1,  "New York City",   "US", 1,  "Obvious #1"),
        (2,  "Chicago",         "US", 3,  "Favored for ranking Top-5 in every category"),
        (3,  "Los Angeles",     "US", 2,  "Build more outwards than upwards"),
        (4,  "Toronto",         "CA", 5,  "Obvious #1 for Canada"),
        (5,  "Dallas",          "US", 4,  "Includes Fort Worth"),
        (6,  "Miami",           "US", 9,  "Full South Florida corridor; will skyrocket up this list"),
        (7,  "Houston",         "US", 6,  None),
        (8,  "San Francisco",   "US", 12, "Includes Oakland and San Jose"),
        (9,  "Atlanta",         "US", 10, None),
        (10, "Boston",          "US", 11, "Largest high-floor low-ceiling city"),
        (11, "Philadelphia",    "US", 8,  None),
        (12, "Seattle",         "US", 16, "Construction boom; benefits from boom in Bellevue too"),
        (13, "Denver",          "US", 20, None),
        (14, "Minneapolis",     "US", 17, "Includes St. Paul"),
        (15, "Detroit",         "US", 14, "As of 2021, all 4 teams play in the city center"),
        (16, "Montreal",        "CA", 15, "Most likely reached its ceiling due to height restrictions"),
        (17, "Las Vegas",       "US", 31, "Counting the A's; will certainly get an NBA team"),
        (18, "Washington DC",   "US", 7,  "Much lower due to lack of hi-rises; skyline credited to NoVA"),
        (19, "Charlotte",       "US", 24, None),
        (20, "Vancouver",       "CA", 23, "Construction in other suburbs gives a massive boost"),
        (21, "Tampa",           "US", 19, "Includes St. Petersburg; Rays will build new downtown ballpark"),
        (22, "Baltimore",       "US", 22, None),
        (23, "Phoenix",         "US", 13, "Most disappointing skyline relative to city size"),
        (24, "Pittsburgh",      "US", 28, "Black and yellow color scheme for every team"),
        (25, "Calgary",         "CA", 44, "Most noticeable discrepancy between city size and cityscape"),
        (26, "San Diego",       "US", 18, "Largest metro with only one pro sports team"),
        (27, "St. Louis",       "US", 21, "Lost the Rams to LA, also stupid decision"),
        (28, "Cleveland",       "US", 33, "Smallest metro with 3 pro sports teams"),
        (29, "Nashville",       "US", 37, "Them or Charlotte will likely get an MLB team"),
        (30, "Portland",        "US", 25, "There are talks of MLB expansion here"),
        (31, "Austin",          "US", 35, "Get this city a pro sports team; will skyrocket"),
        (32, "Kansas City",     "US", 32, "Royals might get new ballpark in downtown KC"),
        (33, "Cincinnati",      "US", 30, None),
        (34, "Orlando",         "US", 26, "Disney and Universal traffic"),
        (35, "Indianapolis",    "US", 36, "Also has the Indy 500"),
        (36, "Edmonton",        "CA", 46, None),
        (37, "Columbus",        "US", 34, "Also has The Ohio State University athletics"),
        (38, "San Antonio",     "US", 27, "Victor Wembanyama doesn't count as a hi-rise"),
        (39, "Milwaukee",       "US", 41, "Not counting the Packers; Green Bay is too far"),
        (40, "New Orleans",     "US", 61, "Discrepancy due to population loss from Katrina"),
        (41, "Sacramento",      "US", 29, "If they ever approved anything without red tape, would be higher"),
        (42, "Salt Lake City",  "US", 50, "Coyotes are now the Utah Mammoth"),
        (43, "Jacksonville",    "US", 39, None),
        (44, "Raleigh",         "US", 42, "Also has Duke, NC State, and UNC athletics"),
        (45, "Oklahoma City",   "US", 45, "Stole the Sonics from Seattle; should've been expansion"),
        (46, "Honolulu",        "US", 59, "Very high-floor low-ceiling; needs a higher ceiling"),
        (47, "Buffalo",         "US", 53, "Bills get a new stadium in 2026"),
        (48, "Virginia Beach",  "US", 38, "Includes Norfolk and Portsmouth"),
        (49, "Ottawa",          "CA", 43, None),
        (50, "Hartford",        "US", 54, None),
        (51, "Louisville",      "US", 47, "NBA expansion possible in the future"),
        (52, "Winnipeg",        "CA", 74, "By far the smallest metro with multiple pro sports teams"),
        (53, "Tulsa",           "US", 58, None),
        (54, "Memphis",         "US", 48, "Lowest ranked US city with a pro sports team"),
        (55, "Omaha",           "US", 60, None),
        # Cities in Chris's tail / not in aggregate sheet
        (56, "Albany",          "US", 66, None),
        (57, "Des Moines",      "US", 81, None),
        (58, "Little Rock",     "US", 80, None),
        (59, "Mobile",          "US", 114,None),
        (60, "Quebec City",     "CA", 73, "UNESCO World Heritage historic district; unique outlier"),
    ]
    c.executemany("INSERT INTO cities VALUES (?,?,?,?,?)", cities)

    # ─────────────────────────────────────────────────────────────
    # SKYLINE DATA — verbatim from Chris's sheet
    # Cumulative counts: over_150m includes all buildings >150m
    # over_100m is approximate for top cities ("LMAO"/"LOL" = estimated)
    # topped-out buildings counted per Chris's rule
    # Toronto: +2 at 300m+ (SkyTower @ Pinnacle One Yonge + The One, both U/C topped out)
    # DC: credited with NoVA skyline per discussion
    # ─────────────────────────────────────────────────────────────
    skyline = [
        # city_id, 100m, 150m, 200m, 250m, 300m, 350m, 400m, skyline_rank, notes
        (1,  999, 322, 106, 37, 19, 9, 6, 1,  "100m+ too many to count accurately"),
        (2,  999, 133, 36,  17, 7,  3, 2, 2,  "LOL at trying to count 100m"),
        (3,  60,  35,  13,  3,  2,  0, 0, 6,  "Builds outward not upward"),
        (4,  999, 87,  27,  6,  2,  0, 0, 3,  "2 topped-out 300m+ towers (SkyTower + The One); First Canadian Place is 298m"),
        (5,  50,  24,  6,   1,  0,  0, 0, 10, "Cowboys and Rangers play in Arlington"),
        (6,  150, 86,  11,  1,  0,  0, 0, 4,  "Full South Florida corridor incl Sunny Isles, Fort Lauderdale, Hollywood"),
        (7,  60,  40,  16,  3,  2,  0, 0, 5,  None),
        (8,  60,  27,  5,   2,  1,  0, 0, 7,  "Includes full Bay Area"),
        (9,  40,  18,  9,   3,  1,  0, 0, 11, None),
        (10, 50,  25,  5,   0,  0,  0, 0, 9,  "High floor low ceiling"),
        (11, 57,  17,  7,   4,  1,  0, 0, 12, None),
        (12, 50,  24,  6,   2,  0,  0, 0, 8,  "Bellevue towers included"),
        (13, 39,  8,   3,   0,  0,  0, 0, 19, None),
        (14, 43,  12,  4,   0,  0,  0, 0, 16, None),
        (15, 28,  9,   2,   0,  0,  0, 0, 22, None),
        (16, 67,  11,  3,   0,  0,  0, 0, 15, "Height restrictions likely cap future growth"),
        (17, 50,  17,  2,   0,  0,  0, 0, 14, "Dense resort corridor"),
        (18, 16,  0,   0,   0,  0,  0, 0, 54, "Height Act; skyline credited to NoVA/Rosslyn/Tysons"),
        (19, 27,  8,   3,   1,  0,  0, 0, 21, None),
        (20, 77,  11,  1,   0,  0,  0, 0, 20, "Dense but constrained by mountains"),
        (21, 23,  5,   0,   0,  0,  0, 0, 27, "Growing; Waldorf Astoria will add 300m+ when topped out"),
        (22, 25,  4,   0,   0,  0,  0, 0, 26, None),
        (23, 18,  0,   0,   0,  0,  0, 0, 53, "Classic sprawl penalty"),
        (24, 26,  10,  2,   1,  0,  0, 0, 18, None),
        (25, 50,  18,  5,   0,  0,  0, 0, 13, "Punches way above its weight"),
        (26, 37,  3,   0,   0,  0,  0, 0, 29, "Sea of 25-30 story buildings, nothing tall"),
        (27, 12,  3,   0,   0,  0,  0, 0, 35, None),
        (28, 19,  5,   3,   1,  0,  0, 0, 23, None),
        (29, 30,  4,   0,   0,  0,  0, 0, 25, None),
        (30, 10,  4,   0,   0,  0,  0, 0, 30, None),
        (31, 39,  10,  3,   1,  0,  0, 0, 17, "Waterline and other projects boosted this significantly"),
        (32, 14,  3,   0,   0,  0,  0, 0, 33, None),
        (33, 12,  3,   1,   0,  0,  0, 0, 32, None),
        (34, 8,   0,   0,   0,  0,  0, 0, 57, "Mostly flat; theme park architecture doesn't count"),
        (35, 9,   3,   1,   0,  0,  0, 0, 37, None),
        (36, 24,  2,   1,   1,  0,  0, 0, 31, None),
        (37, 15,  5,   0,   0,  0,  0, 0, 28, None),
        (38, 9,   1,   0,   0,  0,  0, 0, 43, None),
        (39, 13,  4,   0,   0,  0,  0, 0, 34, None),
        (40, 24,  4,   1,   0,  0,  0, 0, 24, None),
        (41, 9,   0,   0,   0,  0,  0, 0, 56, None),
        (42, 10,  0,   0,   0,  0,  0, 0, 55, None),
        (43, 7,   2,   0,   0,  0,  0, 0, 42, None),
        (44, 4,   1,   0,   0,  0,  0, 0, 48, None),
        (45, 7,   3,   1,   1,  0,  0, 0, 38, None),
        (46, 40,  0,   0,   0,  0,  0, 0, 40, "Sea of 25-30 story buildings; nothing over 150m"),
        (47, 5,   1,   0,   0,  0,  0, 0, 46, None),
        (48, 3,   1,   0,   0,  0,  0, 0, 51, "Includes Norfolk and Portsmouth"),
        (49, 8,   0,   0,   0,  0,  0, 0, 58, None),
        (50, 7,   3,   0,   0,  0,  0, 0, 39, None),
        (51, 11,  2,   0,   0,  0,  0, 0, 41, None),
        (52, 6,   1,   0,   0,  0,  0, 0, 44, None),
        (53, 10,  4,   1,   0,  0,  0, 0, 36, None),
        (54, 7,   0,   0,   0,  0,  0, 0, 59, None),
        (55, 2,   1,   0,   0,  0,  0, 0, 50, None),
        # Tail cities from sheet
        (56, 2,   1,   0,   0,  0,  0, 0, 62, None),  # Albany
        (57, 5,   1,   0,   0,  0,  0, 0, 64, None),  # Des Moines
        (58, 5,   1,   0,   0,  0,  0, 0, 63, None),  # Little Rock
        (59, 3,   1,   1,   0,  0,  0, 0, 61, None),  # Mobile
        (60, 3,   0,   0,   0,  0,  0, 0, 65, "UNESCO historic district; Chateau Frontenac is iconic but not tall"),
    ]
    c.executemany("INSERT INTO skyline_data VALUES (?,?,?,?,?,?,?,?,?,?)", skyline)

    # ─────────────────────────────────────────────────────────────
    # AIRPORTS — verbatim from Chris's sheet
    # ─────────────────────────────────────────────────────────────
    airports = [
        # city_id, pax_millions, count, iata, rank, notes
        (1,  62.9, 3, "JFK,EWR,LGA",  1,  "3 airports fairly split; JFK focuses on international"),
        (2,  42.8, 2, "ORD,MDW",       5,  "United hub"),
        (3,  43.8, 4, "LAX,SNA,BUR,ONT", 3, "ONT/IE folded into LA metro"),
        (4,  37.3, 2, "YYZ,YTZ",       7,  None),
        (5,  43.1, 2, "DFW,DAL",       4,  "American hub"),
        (6,  42.6, 3, "MIA,FLL,PBI",   6,  "Gateway to LATAM and the Caribbean"),
        (7,  26.3, 2, "IAH,HOU",       10, None),
        (8,  31.5, 3, "SFO,SJC,OAK",   9,  None),
        (9,  45.4, 1, "ATL",           2,  "Delta hub; single busiest airport on earth"),
        (10, 17.4, 1, "BOS",           18, None),
        (11, 12.4, 1, "PHL",           23, None),
        (12, 22.2, 1, "SEA",           14, None),
        (13, 33.8, 1, "DEN",           8,  "Only other Top-10 city with a single airport"),
        (14, 15.2, 1, "MSP",           20, None),
        (15, 13.8, 1, "DTW",           22, None),
        (16, 16.0, 1, "YUL",           19, None),
        (17, 25.5, 1, "LAS",           11, None),
        (18, 21.8, 2, "DCA,IAD",       16, "BWI excluded; Baltimore is separate metro"),
        (19, 23.1, 1, "CLT",           13, "American hub"),
        (20, 19.0, 1, "YVR",           17, "Canada's hub for Asia-Pacific"),
        (21, 10.5, 1, "TPA",           27, "Has a GIANT FLAMINGO"),
        (22, 11.2, 1, "BWI",           25, None),
        (23, 21.9, 1, "PHX",           15, None),
        (24, 3.9,  1, "PIT",           41, None),
        (25, 14.5, 1, "YYC",           21, None),
        (26, 11.1, 1, "SAN",           26, None),
        (27, 6.7,  1, "STL",           32, None),
        (28, 4.2,  1, "CLE",           39, None),
        (29, 9.8,  1, "BNA",           29, None),
        (30, 7.2,  1, "PDX",           31, None),
        (31, 10.3, 1, "AUS",           28, None),
        (32, 4.8,  1, "MCI",           37, None),
        (33, 3.7,  1, "CVG",           42, None),
        (34, 24.5, 1, "MCO",           12, "Disney and Universal traffic"),
        (35, 4.2,  1, "IND",           40, None),
        (36, 5.8,  1, "YEG",           36, None),
        (37, 3.6,  1, "CMH",           43, None),
        (38, 4.8,  1, "SAT",           38, None),
        (39, 2.7,  1, "MKE",           48, None),
        (40, 5.9,  1, "MSY",           34, None),
        (41, 6.0,  1, "SMF",           33, None),
        (42, 12.4, 1, "SLC",           24, None),
        (43, 3.2,  1, "JAX",           44, None),
        (44, 5.9,  1, "RDU",           35, None),
        (45, 2.0,  1, "OKC",           53, None),
        (46, 8.8,  1, "HNL",           30, None),
        (47, 2.0,  1, "BUF",           52, None),
        (48, 2.1,  1, "ORF",           51, "Includes Norfolk"),
        (49, 3.0,  1, "YOW",           45, None),
        (50, 2.8,  1, "BDL",           47, None),
        (51, 1.9,  1, "SDF",           54, None),
        (52, 3.0,  1, "YWG",           46, None),
        (53, 1.4,  1, "TUL",           55, None),
        (54, 2.2,  1, "MEM",           50, None),
        (55, 2.2,  1, "OMA",           49, None),
        # Tail cities — estimated
        (56, 1.2,  1, "ALB",           57, None),  # Albany
        (57, 3.0,  1, "DSM",           56, None),  # Des Moines
        (58, 3.0,  1, "LIT",           58, None),  # Little Rock
        (59, 0.8,  1, "MOB",           60, None),  # Mobile
        (60, 1.8,  1, "YQB",           59, None),  # Quebec City
    ]
    c.executemany("INSERT INTO airports VALUES (?,?,?,?,?,?)", airports)

    # ─────────────────────────────────────────────────────────────
    # SPORTS — verbatim from Chris's sheet
    # ─────────────────────────────────────────────────────────────
    sports = [
        # city_id, nfl, nba, mlb, nhl, big4_total, sports_rank, notes
        (1,  2, 2, 2, 3, 9, 1,  "NJ home for 3 teams"),
        (2,  1, 1, 2, 1, 5, 3,  "Forgot about the White Sox LOL"),
        (3,  2, 2, 2, 2, 8, 2,  "Orange County has 2 teams"),
        (4,  0, 1, 1, 1, 3, 4,  "Counting Hamilton in GTA; no NFL"),  # Raptors, Blue Jays, Leafs
        (5,  1, 1, 1, 1, 4, 5,  "Cowboys and Rangers play in Arlington"),
        (6,  1, 1, 1, 1, 4, 8,  "Panthers play closer to Fort Lauderdale"),
        (7,  1, 1, 1, 0, 3, 15, "Might get an NHL team soon"),
        (8,  1, 1, 1, 1, 4, 10, "Spread across 3 cities and 2 counties"),
        (9,  1, 1, 1, 0, 3, 16, "Lost Thrashers (NHL) to Winnipeg"),
        (10, 1, 1, 1, 1, 4, 9,  "Patriots play in Foxborough, closer to Providence"),
        (11, 1, 1, 1, 1, 4, 7,  "All teams currently share the same parking lot"),
        (12, 1, 0, 1, 1, 3, 17, "Sonics 100% returning before 2030"),
        (13, 1, 1, 1, 1, 4, 14, "Smallest metro with the Big-4"),
        (14, 1, 1, 1, 1, 4, 13, "All team names start with Minnesota"),
        (15, 1, 1, 1, 1, 4, 12, "As of 2021, all 4 teams play in city center"),
        (16, 0, 0, 1, 1, 2, 22, "Lost the Expos (MLB) to Washington DC"),
        (17, 1, 0, 1, 1, 3, 20, "Counting A's; will certainly get NBA team"),
        (18, 1, 1, 1, 1, 4, 6,  "Commanders play in Maryland, will return to DC"),
        (19, 1, 0, 0, 0, 1, 26, "Both teams are poverty franchises"),  # Panthers + Hornets
        (20, 0, 0, 0, 1, 1, 23, "Lost the Grizzlies (NBA) to Memphis"),
        (21, 1, 0, 0, 1, 2, 18, "All team names start with Tampa Bay; Rays new ballpark coming"),
        (22, 1, 0, 1, 0, 2, 24, None),
        (23, 1, 1, 1, 0, 3, 16, "Lost the Coyotes to SLC"),
        (24, 1, 0, 1, 1, 3, 19, None),
        (25, 0, 0, 0, 1, 1, 32, None),
        (26, 0, 0, 1, 0, 1, 37, "Lost the Chargers to LA; largest metro with only one pro team"),
        (27, 0, 0, 1, 1, 2, 23, "Lost the Rams to LA; also stupid decision"),
        (28, 1, 1, 1, 0, 3, 21, "Smallest metro with 3 pro sports teams"),
        (29, 1, 0, 0, 1, 2, 30, "Them or Charlotte will likely get MLB"),
        (30, 0, 1, 0, 0, 1, 38, "Talks of MLB expansion"),
        (31, 0, 0, 0, 0, 0, 49, "Largest city without a Big 4 team by far"),
        (32, 1, 0, 1, 0, 2, 28, "Almost got the Penguins (NHL)"),
        (33, 1, 0, 1, 0, 2, 27, None),
        (34, 0, 1, 0, 0, 1, 39, "Tampa Bay lacks NBA; Orlando has it"),
        (35, 1, 1, 0, 0, 2, 29, "Also has the Indy 500"),
        (36, 0, 0, 0, 1, 1, 33, None),
        (37, 0, 0, 0, 1, 1, 42, "Also has Ohio State athletics"),
        (38, 0, 1, 0, 0, 1, 40, "Victor Wembanyama doesn't count as a hi-rise"),
        (39, 0, 1, 1, 0, 2, 31, "Not counting Packers; Green Bay too far"),
        (40, 1, 1, 0, 0, 2, 35, "Pelicans most likely NBA team to relocate"),
        (41, 0, 1, 0, 0, 1, 41, "Beam should count as a second team; A's temporarily here"),
        (42, 0, 1, 0, 1, 2, 34, "Coyotes are now the Utah Mammoth"),
        (43, 1, 0, 0, 0, 1, 39, None),  # Jaguars
        (44, 0, 0, 0, 1, 1, 44, "Also has Duke, NC State, UNC"),
        (45, 0, 1, 0, 0, 1, 46, "Stole the Sonics from Seattle"),
        (46, 0, 0, 0, 0, 0, 54, "No major pro teams"),
        (47, 1, 0, 0, 0, 1, 34, "Bills get new stadium in 2026"),
        (48, 0, 0, 0, 0, 0, 50, "Worthy of a Big 4 team"),
        (49, 0, 0, 0, 1, 1, 45, None),  # Senators
        (50, 0, 0, 0, 0, 0, 52, None),
        (51, 0, 0, 0, 0, 0, 47, "NBA expansion possible"),
        (52, 0, 0, 0, 1, 1, 36, "Far smallest metro with multiple pro sports"),  # Jets + NHL
        (53, 0, 0, 0, 0, 0, 53, None),
        (54, 0, 1, 0, 0, 1, 47, "Lowest ranked US city with a pro sports team"),  # Grizzlies
        (55, 0, 0, 0, 0, 0, 55, None),
        # Tail cities
        (56, 0, 0, 0, 0, 0, 58, None),  # Albany
        (57, 0, 0, 0, 0, 0, 57, None),  # Des Moines
        (58, 0, 0, 0, 0, 0, 59, None),  # Little Rock
        (59, 0, 0, 0, 0, 0, 60, None),  # Mobile
        (60, 0, 0, 0, 0, 0, 56, None),  # Quebec City
    ]
    c.executemany("INSERT INTO sports_teams VALUES (?,?,?,?,?,?,?,?)", sports)

    # ─────────────────────────────────────────────────────────────
    # PHASE 2: TRANSIT RIDERSHIP (annual riders, heavy rail only)
    # ─────────────────────────────────────────────────────────────
    transit = [
        (1,  "NYC Subway",              1600000000),
        (2,  "CTA Rail",                 165000000),
        (3,  "LA Metro Rail",            100000000),
        (4,  "TTC Subway",               200000000),
        (5,  "DART",                      18000000),
        (6,  "Miami Metrorail",           20000000),
        (7,  "Houston METRORail",         15000000),
        (8,  "BART + Muni Metro",        130000000),
        (9,  "MARTA Rail",                58000000),
        (10, "MBTA Subway",              120000000),
        (11, "SEPTA Rail",                80000000),
        (12, "Sound Transit Link",        27000000),
        (13, "RTD Rail",                  20000000),
        (14, "Metro Transit LRT",         30000000),
        (15, "Detroit People Mover",       2000000),
        (16, "STM Metro",                200000000),
        (17, "Las Vegas Monorail",          5000000),
        (18, "DC Metro",                 165000000),
        (19, "CATS Light Rail",            12000000),
        (20, "SkyTrain",                 145000000),
        (21, "HART",                       5000000),
        (22, "Baltimore Metro/Light Rail", 14000000),
        (23, "Valley Metro Rail",          16000000),
        (24, "Port Authority T",           25000000),
        (25, "CTrain",                     65000000),
        (26, "MTS Trolley",               12000000),
        (27, "MetroLink",                  14000000),
        (28, "RTA Rail",                    8000000),
        (29, "WeGo/Nashville SC",           1000000),
        (30, "MAX Light Rail",             38000000),
        (31, "Capital Metro",               3000000),
        (32, "KC Streetcar",                1000000),
        (33, "Cincinnati Bell Connector",     500000),
        (34, "SunRail",                     3000000),
        (35, "IndyGo Red Line",             1000000),
        (36, "Edmonton LRT",               22000000),
        (37, "COTA",                        1000000),
        (38, "VIA Metro",                       0),
        (39, "Milwaukee Streetcar",           500000),
        (40, "New Orleans Streetcar",         5000000),
        (41, "Sacramento RT Light Rail",     10000000),
        (42, "TRAX",                        17000000),
        (43, "JTA Skyway",                   1000000),
        (44, "GoRaleigh",                      500000),
        (45, "Oklahoma City Streetcar",        500000),
        (46, "TheBus",                       5000000),
        (47, "NFTA Metro Rail",              4000000),
        (48, "HRT",                          3000000),
        (49, "OC Transpo O-Train",          15000000),
        (50, "CTtransit",                    1000000),
        (51, "TARC",                         1000000),
        (52, "Winnipeg Transit",             3000000),
        (53, "Tulsa Transit",                  500000),
        (54, "MATA",                         2000000),
        (55, "Omaha Metro",                    500000),
        (56, "CDTA",                         1000000),
        (57, "DART Des Moines",               500000),
        (58, "Rock Region Metro",              500000),
        (59, "Wave Transit",                   300000),
        (60, "RTC Quebec",                    1000000),
    ]
    c.executemany("INSERT INTO transit_systems VALUES (?,?,?)", transit)

    # ─────────────────────────────────────────────────────────────
    # PHASE 2: CONVENTION CENTERS (sq ft)
    # ─────────────────────────────────────────────────────────────
    convention = [
        (1,  "Jacob K. Javits Center",               855000),
        (2,  "McCormick Place",                      2600000),
        (3,  "Los Angeles Convention Center",         720000),
        (4,  "Metro Toronto Convention Centre",       600000),
        (5,  "Kay Bailey Hutchison Convention Ctr",  1000000),
        (6,  "Miami Beach / Broward Combined",        700000),
        (7,  "George R. Brown Convention Center",     860000),
        (8,  "Moscone Center",                        442000),
        (9,  "Georgia World Congress Center",        1400000),
        (10, "Boston Convention & Exhibition Ctr",    516000),
        (11, "Pennsylvania Convention Center",        679000),
        (12, "Washington State Convention Center",    415000),
        (13, "Colorado Convention Center",            584000),
        (14, "Minneapolis Convention Center",         480000),
        (15, "Huntington Place",                      700000),
        (16, "Palais des congres de Montreal",        552000),
        (17, "Las Vegas Convention Center",          4600000),
        (18, "Walter E. Washington Convention Ctr",   703000),
        (19, "Charlotte Convention Center",           280000),
        (20, "Vancouver Convention Centre",           466000),
        (21, "Tampa Convention Center",               200000),
        (22, "Baltimore Convention Center",           300000),
        (23, "Phoenix Convention Center",             900000),
        (24, "David L. Lawrence Convention Center",   330000),
        (25, "BMO Centre",                            230000),
        (26, "San Diego Convention Center",           615000),
        (27, "America's Center",                      502000),
        (28, "Huntington Convention Center",          225000),
        (29, "Music City Center",                     353000),
        (30, "Oregon Convention Center",              255000),
        (31, "Austin Convention Center",              247000),
        (32, "Kansas City Convention Center",         388000),
        (33, "Duke Energy Convention Center",         200000),
        (34, "Orange County Convention Center",      2100000),
        (35, "Indiana Convention Center",             566000),
        (36, "Edmonton Convention Centre",            170000),
        (37, "Greater Columbus Convention Center",    436000),
        (38, "Henry B. Gonzalez Convention Center",   514000),
        (39, "Wisconsin Center",                      188000),
        (40, "Ernest N. Morial Convention Center",    700000),
        (41, "Sacramento Convention Center",          175000),
        (42, "Salt Palace Convention Center",         515000),
        (43, "Prime Osborn Convention Center",         78000),
        (44, "Raleigh Convention Center",             150000),
        (45, "Cox Convention Center",                 100000),
        (46, "Hawaii Convention Center",              200000),
        (47, "Buffalo Niagara Convention Center",      76000),
        (48, "Virginia Beach Convention Center",      150000),
        (49, "Shaw Centre",                           120000),
        (50, "Connecticut Convention Center",         140000),
        (51, "Kentucky International Convention Ctr", 130000),
        (52, "RBC Convention Centre",                 120000),
        (53, "Cox Business Center",                   100000),
        (54, "Memphis Cook Convention Center",        120000),
        (55, "CenturyLink Center Omaha",              194000),
        (56, "Albany Capital Center",                  82000),
        (57, "Iowa Events Center",                    150000),
        (58, "Statehouse Convention Center",          117000),
        (59, "Mobile Convention Center",               90000),
        (60, "Centre des congres de Quebec",          200000),
    ]
    c.executemany("INSERT INTO convention_centers VALUES (?,?,?)", convention)

    # ─────────────────────────────────────────────────────────────
    # PHASE 2: CORPORATE HQs (Fortune 500 / TSX equivalent)
    # ─────────────────────────────────────────────────────────────
    hq = [
        (1,  57, "Finance, media, pharma dominant"),
        (2,  21, None),
        (3,  5,  "Tech in Silicon Beach but HQs sparse"),
        (4,  18, "TSX equivalent weighting"),
        (5,  12, None),
        (6,  4,  None),
        (7,  23, "Energy sector dominant"),
        (8,  14, "Tech giants HQ in Bay Area"),
        (9,  9,  None),
        (10, 6,  None),
        (11, 9,  None),
        (12, 7,  "Tech + biotech"),
        (13, 5,  None),
        (14, 10, None),
        (15, 5,  None),
        (16, 6,  None),
        (17, 1,  "Gaming + hospitality dominant"),
        (18, 8,  "Government adjacent"),
        (19, 3,  None),
        (20, 4,  None),
        (21, 2,  None),
        (22, 2,  None),
        (23, 3,  None),
        (24, 5,  "PNC, US Steel, PPG"),
        (25, 8,  "Energy sector: Suncor, TC Energy"),
        (26, 2,  None),
        (27, 9,  "Anheuser-Busch, Edward Jones"),
        (28, 3,  None),
        (29, 2,  None),
        (30, 2,  "Nike nearby in Beaverton"),
        (31, 3,  "Dell, Tesla TX HQ, Oracle TX HQ"),
        (32, 3,  None),
        (33, 3,  None),
        (34, 1,  None),
        (35, 4,  "Eli Lilly, Salesforce tower"),
        (36, 4,  "Energy: Imperial Oil, Canadian Natural"),
        (37, 4,  None),
        (38, 3,  None),
        (39, 2,  None),
        (40, 1,  None),
        (41, 2,  None),
        (42, 2,  None),
        (43, 1,  None),
        (44, 2,  "Red Hat, Citrix"),
        (45, 1,  None),
        (46, 0,  None),
        (47, 1,  None),
        (48, 1,  None),
        (49, 3,  "Government + Shopify HQ"),
        (50, 4,  "United Healthcare, Aetna"),
        (51, 2,  None),
        (52, 1,  None),
        (53, 1,  None),
        (54, 1,  None),
        (55, 2,  "Berkshire Hathaway HQ"),
        (56, 0,  None),
        (57, 1,  None),
        (58, 0,  None),
        (59, 0,  None),
        (60, 0,  None),
    ]
    c.executemany("INSERT INTO corporate_hq VALUES (?,?,?)", hq)

    # ─────────────────────────────────────────────────────────────
    # PHASE 2: LANDMARKS
    # Tier 1=world-famous(10pts), Tier 2=nationally known(5pts), Tier 3=regional(2pts)
    # ─────────────────────────────────────────────────────────────
    landmarks = [
        # NYC
        (1, "Statue of Liberty", 1, 0), (1, "Empire State Building", 1, 0),
        (1, "Central Park", 1, 1), (1, "Brooklyn Bridge", 1, 0),
        (1, "Times Square", 1, 0), (1, "One World Trade Center", 2, 0),
        (1, "High Line", 3, 0), (1, "Rockefeller Center", 2, 0),
        # Chicago
        (2, "Cloud Gate (The Bean)", 1, 0), (2, "Millennium Park", 2, 0),
        (2, "Navy Pier", 2, 0), (2, "Willis Tower", 2, 0),
        (2, "Chicago Riverwalk", 3, 0), (2, "Wrigley Field", 2, 0),
        # LA
        (3, "Hollywood Sign", 1, 0), (3, "Venice Beach", 2, 1),
        (3, "Griffith Observatory", 2, 0), (3, "Santa Monica Pier", 2, 0),
        (3, "Disneyland", 1, 0), (3, "Getty Center", 3, 0),
        # Toronto
        (4, "CN Tower", 1, 0), (4, "Niagara Falls (proximity)", 1, 1),
        (4, "Distillery District", 3, 0), (4, "Toronto Islands", 3, 1),
        # Dallas
        (5, "Sixth Floor Museum / Dealey Plaza", 2, 0),
        (5, "AT&T Stadium", 2, 0), (5, "Reunion Tower", 3, 0),
        # Miami
        (6, "South Beach / Ocean Drive", 1, 0),
        (6, "Art Deco Historic District", 2, 0),
        (6, "Everglades (proximity)", 2, 1),
        (6, "Wynwood Walls", 3, 0), (6, "Vizcaya Museum", 3, 0),
        # Houston
        (7, "NASA Johnson Space Center", 2, 0),
        (7, "Buffalo Bayou Park", 3, 1),
        # SF
        (8, "Golden Gate Bridge", 1, 0), (8, "Alcatraz Island", 1, 0),
        (8, "Fisherman's Wharf", 2, 0), (8, "Lombard Street", 2, 0),
        (8, "Muir Woods (proximity)", 2, 1), (8, "Cable Cars", 2, 0),
        # Atlanta
        (9, "World of Coca-Cola", 2, 0), (9, "MLK Jr. National Historic Site", 2, 0),
        (9, "Stone Mountain", 2, 1), (9, "CNN Center", 3, 0),
        # Boston
        (10, "Freedom Trail", 2, 0), (10, "Fenway Park", 2, 0),
        (10, "Harvard University", 2, 0), (10, "Boston Common", 3, 0),
        # Philadelphia
        (11, "Liberty Bell", 1, 0), (11, "Independence Hall", 1, 0),
        (11, "Rocky Steps / Philadelphia Museum", 2, 0),
        (11, "Reading Terminal Market", 3, 0),
        # Seattle
        (12, "Space Needle", 1, 0), (12, "Pike Place Market", 2, 0),
        (12, "Mount Rainier (proximity)", 2, 1),
        (12, "Chihuly Garden and Glass", 3, 0),
        # Denver
        (13, "Rocky Mountain National Park (proximity)", 1, 1),
        (13, "Red Rocks Amphitheatre", 2, 0),
        (13, "Denver Art Museum", 3, 0),
        # Minneapolis
        (14, "Mall of America", 2, 0), (14, "Stone Arch Bridge", 3, 0),
        (14, "Boundary Waters (proximity)", 3, 1),
        # Detroit
        (15, "Motown Museum", 2, 0), (15, "Detroit Institute of Arts", 3, 0),
        (15, "Ambassador Bridge", 3, 0),
        # Montreal
        (16, "Mount Royal Park", 2, 1),
        (16, "Old Montreal / Notre-Dame Basilica", 2, 0),
        (16, "Montreal Botanical Garden", 3, 0),
        (16, "Jean-Talon Market", 3, 0),
        # Las Vegas
        (17, "The Strip", 1, 0), (17, "Fremont Street Experience", 2, 0),
        (17, "Welcome to Las Vegas Sign", 2, 0),
        (17, "Grand Canyon (proximity)", 1, 1),
        (17, "Hoover Dam (proximity)", 2, 0),
        (17, "Red Rock Canyon", 2, 1),
        # DC
        (18, "National Mall", 1, 0), (18, "Washington Monument", 1, 0),
        (18, "Lincoln Memorial", 1, 0), (18, "US Capitol", 1, 0),
        (18, "White House", 1, 0), (18, "Smithsonian Museums", 2, 0),
        (18, "Arlington Cemetery", 2, 0),
        # Charlotte
        (19, "NASCAR Hall of Fame", 3, 0), (19, "US National Whitewater Center", 3, 1),
        # Vancouver
        (20, "Stanley Park", 1, 1), (20, "Capilano Suspension Bridge", 2, 0),
        (20, "Granville Island", 2, 0), (20, "Grouse Mountain", 2, 1),
        (20, "Whistler (proximity)", 2, 1),
        # Tampa
        (21, "Busch Gardens", 2, 0), (21, "Ybor City", 3, 0),
        (21, "Clearwater Beach", 2, 1),
        # Baltimore
        (22, "Inner Harbor", 2, 0), (22, "Fort McHenry", 2, 0),
        (22, "National Aquarium", 3, 0),
        # Phoenix
        (23, "Grand Canyon (proximity)", 1, 1),
        (23, "Camelback Mountain", 2, 1),
        (23, "Desert Botanical Garden", 3, 1),
        # Pittsburgh
        (24, "Point State Park", 3, 0), (24, "Carnegie Museums", 3, 0),
        (24, "Fallingwater (proximity)", 2, 0),
        # Calgary
        (25, "Banff National Park (proximity)", 1, 1),
        (25, "Canadian Rockies (proximity)", 1, 1),
        (25, "Calgary Stampede Grounds", 2, 0),
        (25, "Heritage Park", 3, 0),
        # San Diego
        (26, "Balboa Park / San Diego Zoo", 2, 0),
        (26, "USS Midway Museum", 2, 0),
        (26, "La Jolla Cove", 2, 1),
        # St. Louis
        (27, "Gateway Arch", 1, 0), (27, "Busch Stadium", 3, 0),
        # Cleveland
        (28, "Rock and Roll Hall of Fame", 2, 0),
        (28, "Lake Erie waterfront", 3, 1),
        # Nashville
        (29, "Broadway Honky Tonks", 2, 0),
        (29, "Country Music Hall of Fame", 2, 0),
        (29, "Grand Ole Opry", 2, 0),
        # Portland
        (30, "Powell's Books", 3, 0), (30, "Mount Hood (proximity)", 2, 1),
        (30, "Columbia River Gorge", 2, 1),
        # Austin
        (31, "6th Street", 2, 0), (31, "South by Southwest (SXSW)", 2, 0),
        (31, "Barton Springs", 3, 1),
        # Kansas City
        (32, "National WWI Museum", 2, 0),
        (32, "Country Club Plaza", 3, 0),
        # Cincinnati
        (33, "Cincinnati Music Hall", 3, 0),
        (33, "National Underground Railroad Freedom Center", 3, 0),
        # Orlando
        (34, "Walt Disney World", 1, 0),
        (34, "Universal Studios Florida", 2, 0),
        (34, "Kennedy Space Center (proximity)", 2, 0),
        # Indianapolis
        (35, "Indianapolis Motor Speedway", 2, 0),
        (35, "Children's Museum of Indianapolis", 3, 0),
        # Edmonton
        (36, "West Edmonton Mall", 2, 0),
        (36, "Valley of the Dinosaurs (proximity)", 3, 1),
        # Columbus
        (37, "Ohio State University Campus", 2, 0),
        (37, "Short North Arts District", 3, 0),
        # San Antonio
        (38, "The Alamo", 1, 0), (38, "San Antonio River Walk", 2, 0),
        # Milwaukee
        (39, "Milwaukee Art Museum", 3, 0), (39, "Harley-Davidson Museum", 3, 0),
        # New Orleans
        (40, "French Quarter", 1, 0), (40, "Bourbon Street", 2, 0),
        (40, "Garden District", 2, 0), (40, "Mardi Gras (event)", 1, 0),
        # Sacramento
        (41, "California State Capitol", 2, 0),
        (41, "Old Sacramento Waterfront", 3, 0),
        # Salt Lake City
        (42, "Temple Square", 2, 0),
        (42, "Great Salt Lake", 2, 1),
        (42, "Bonneville Salt Flats (proximity)", 2, 1),
        (42, "Park City / Wasatch Mountains", 2, 1),
        # Jacksonville
        (43, "Timucuan Ecological Preserve", 3, 1),
        (43, "St. Augustine (proximity)", 3, 0),
        # Raleigh
        (44, "Research Triangle Park", 3, 0),
        # Oklahoma City
        (45, "Oklahoma City National Memorial", 2, 0),
        (45, "Bricktown", 3, 0),
        # Honolulu
        (46, "Waikiki Beach", 1, 1), (46, "Diamond Head", 1, 1),
        (46, "Pearl Harbor / USS Arizona Memorial", 1, 0),
        (46, "North Shore", 2, 1),
        # Buffalo
        (47, "Niagara Falls (proximity)", 1, 1),
        (47, "Frank Lloyd Wright Darwin Martin House", 3, 0),
        # Virginia Beach
        (48, "Virginia Beach Oceanfront", 2, 1),
        (48, "Colonial Williamsburg (proximity)", 2, 0),
        # Ottawa
        (49, "Parliament Hill", 1, 0), (49, "Rideau Canal", 2, 1),
        (49, "National Gallery of Canada", 3, 0),
        # Hartford
        (50, "Mark Twain House", 3, 0),
        # Louisville
        (51, "Churchill Downs / Kentucky Derby", 2, 0),
        (51, "Louisville Slugger Museum", 3, 0),
        # Winnipeg
        (52, "The Forks", 3, 0), (52, "Canadian Museum for Human Rights", 3, 0),
        # Tulsa
        (53, "Philbrook Museum of Art", 3, 0),
        (53, "Blue Dome District", 3, 0),
        # Memphis
        (54, "Beale Street", 2, 0), (54, "Graceland", 2, 0),
        (54, "National Civil Rights Museum", 2, 0),
        # Omaha
        (55, "Henry Doorly Zoo", 2, 0), (55, "Old Market District", 3, 0),
        # Albany
        (56, "New York State Capitol", 3, 0),
        # Des Moines
        (57, "Iowa State Capitol", 3, 0),
        # Little Rock
        (58, "Clinton Presidential Library", 3, 0),
        # Mobile
        (59, "USS Alabama Battleship Memorial", 3, 0),
        (59, "Mobile Carnival Museum", 3, 0),
        # Quebec City
        (60, "Old Quebec (UNESCO World Heritage)", 1, 0),
        (60, "Chateau Frontenac", 1, 0),
        (60, "Plains of Abraham", 2, 0),
        (60, "Old Port of Quebec", 2, 0),
    ]
    c.executemany("INSERT INTO landmarks (city_id, name, tier, natural) VALUES (?,?,?,?)", landmarks)

    conn.commit()
    conn.close()
    print(f"✅ Database v2 built: {DB_PATH}")
    print(f"   60 cities | 8 tables | Chris's curated data + Phase 2 estimates")

if __name__ == "__main__":
    build()
