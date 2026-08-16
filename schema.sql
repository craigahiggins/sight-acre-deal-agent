CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    sector TEXT NOT NULL,
    location TEXT,
    source TEXT,
    asking_price REAL,
    potential_value REAL,
    strategic_fit INTEGER DEFAULT 0,
    return_potential INTEGER DEFAULT 0,
    entry_price_score INTEGER DEFAULT 0,
    financeability INTEGER DEFAULT 0,
    asset_backing INTEGER DEFAULT 0,
    synergies INTEGER DEFAULT 0,
    deal_probability INTEGER DEFAULT 0,
    seller_motivation INTEGER DEFAULT 0,
    execution_complexity INTEGER DEFAULT 0,
    score INTEGER DEFAULT 0,
    grade TEXT DEFAULT 'C',
    status TEXT DEFAULT 'New',
    summary TEXT,
    red_flags TEXT,
    recommended_action TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS approvals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deal_id INTEGER NOT NULL,
    action_type TEXT NOT NULL,
    proposed_action TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(deal_id) REFERENCES deals(id)
);
