import sqlite3
from contextlib import contextmanager
from app.config import settings

def init_db():
    """Initializes the database tables with proper schema, indexes, and session isolation."""
    db_path = settings.DB_PATH
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Earnings Table with session_id
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS earnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL DEFAULT 'default',
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                platform TEXT NOT NULL,
                gross_earnings REAL NOT NULL,
                tips_incentives REAL NOT NULL DEFAULT 0.0,
                expenses REAL NOT NULL DEFAULT 0.0,
                net_earnings REAL NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Grievances Table with session_id
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grievances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL DEFAULT 'default',
                category TEXT NOT NULL,
                employer_platform TEXT NOT NULL,
                incident_date TEXT NOT NULL,
                amount_disputed REAL,
                linked_earning_id INTEGER,
                incident_details TEXT NOT NULL,
                evidence_available TEXT,
                generated_draft TEXT NOT NULL,
                language TEXT DEFAULT 'en',
                status TEXT DEFAULT 'draft',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (linked_earning_id) REFERENCES earnings(id) ON DELETE SET NULL
            )
        """)

        # Document Analysis History Table with session_id
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL DEFAULT 'default',
                filename TEXT NOT NULL,
                file_type TEXT NOT NULL,
                extracted_text TEXT NOT NULL,
                summary TEXT NOT NULL,
                key_amounts TEXT,
                important_dates TEXT,
                conditions TEXT,
                checklist TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Chat History Table with session_id
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                language TEXT DEFAULT 'en',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Migrations check: Ensure session_id column exists on existing tables if upgraded
        for table in ["earnings", "grievances", "document_analyses"]:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]
            if "session_id" not in columns:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN session_id TEXT NOT NULL DEFAULT 'default'")

        # Indexes for fast querying & secure session scoping
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_earnings_session ON earnings(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_earnings_date ON earnings(session_id, date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_grievances_session ON grievances(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_doc_session ON document_analyses(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_session ON chat_messages(session_id)")

        conn.commit()

def check_db_health() -> bool:
    """Verifies that the database is accessible and responsive with a live query."""
    try:
        with sqlite3.connect(settings.DB_PATH, timeout=2.0) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
            return row is not None and row[0] == 1
    except Exception:
        return False

@contextmanager
def get_db():
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
