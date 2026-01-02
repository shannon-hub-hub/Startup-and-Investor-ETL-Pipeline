CREATE TABLE startups (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    website TEXT,
    industry TEXT,
    locarion TEXT
);

CREATE TABLE investors (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    website TEXT,
    industry TEXT,
    check_size_min INTEGER,
    check_size_max INTEGER,
    target_countries TEXT
);

CREATE TABLE funding_rounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    startup_id INTEGER,
    investor_id INTEGER,
    amount INTEGER,
    stage TEXT,
    date TEXT,
    FOREIGN KEY (startup_id) REFERENCES startups(id),
    FOREIGN KEY (investor_id) REFERENCES investors(id)
);
