
-- Table Drakon-automate (Procedure like "Attention_Block")
CREATE TABLE drakon_automats (
    automat_id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

-- Table Icon (Node graf algorithm)
CREATE TABLE drakon_icons (
    icon_id INTEGER PRIMARY KEY.
    automat_id INTEGER,
    ikon_type TEXT,		-- 'ACTION' (Todo), 'QUESTION' (Question), 'BRANCH' (Branch)
    label_text TEXT,		-- Symbol expression / Formula Nikomaha
    FOREIGN KEY(automat_id) REFERENCES drakon_automats(automat_id)
);

-- Table Edges (Move beetwin icons - Graf Pascale springs)
CREATE TABLE drakon_edges (
    edge_id INTEGER PRIMARY KEY,
    from_icon_id INTEGER,
    to_icon_id INTEGER,
    condition_value INTEGER,	-- Ternary marker of Setun -1 (Branch "Not", +1 (Branch "Yes"), 0 (Direct move)
    FOREIGN KEY(from_icon_id) REFERENCES drakon_icons(icon_id),
    FOREIGN KEY(to_icon_id) REFERENCES drakon_icons(icon_id)
);


CREATE TABLE electrodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_boundary INTEGER NOT NULL,
    phonon_modulation REAL DEFAULT 0.0
);


CREATE TABLE polymer_threads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phase_mask INTEGER NOT NULL,
    octanion_basis INTEGER NOT NULL CHECK(octanion_basis BETWEEN 0 AND 7)
);


CREATE TABLE memristors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    electrode_id INTEGER,
    thread_id INTEGER,
    ternary_state INTEGER NOT NULL CHECK(ternary_state IN (-1, 0, 1)),
    polytope_rank INTEGER DEFAULT 1,
    epoch TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(electrode_id) REFERENCES electrodes(id),
    FOREIGN KEY(thread_id) REFERENCES polymer_threads(id)
);

