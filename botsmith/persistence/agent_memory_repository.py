# botsmith/persistence/agent_memory_repository.py

import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, Any, List

from botsmith.core.memory.models import AgentMemory, MemoryScope
from botsmith.persistence.database import get_connection


class AgentMemoryRepository:
    """
    SQLite-backed persistent store for scoped memory segments.
    """

    def __init__(self, db_path=None):
        self.db_path = db_path

    def init_schema(self):
        conn = get_connection(self.db_path)
        cur = conn.cursor()

        # Legacy table kept for migration safety
        cur.execute("""
        CREATE TABLE IF NOT EXISTS agent_memory (
            agent_id TEXT PRIMARY KEY,
            interactions TEXT,
            metadata TEXT,
            last_updated TEXT
        )
        """)

        # New scoped memory table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS memory_store (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scope TEXT,
            key TEXT,
            value TEXT,
            version INTEGER,
            updated_at TEXT,
            source TEXT,
            confidence REAL,
            metadata TEXT,
            UNIQUE(scope, key)
        )
        """)

        conn.commit()
        conn.close()

    def save_entry(self, scope: MemoryScope, key: str, value: Any, meta: Dict[str, Any]):
        conn = get_connection(self.db_path)
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO memory_store (scope, key, value, version, updated_at, source, confidence, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(scope, key) DO UPDATE SET
            value=excluded.value,
            version=excluded.version,
            updated_at=excluded.updated_at,
            source=excluded.source,
            confidence=excluded.confidence,
            metadata=excluded.metadata
        """, (
            scope.value,
            key,
            json.dumps(value),
            meta.get("version", 1),
            meta.get("updated_at", datetime.utcnow().isoformat()),
            meta.get("source", "system"),
            meta.get("confidence", 1.0),
            json.dumps(meta)
        ))

        conn.commit()
        conn.close()

    def load_scope(self, scope: MemoryScope) -> Dict[str, Dict[str, Any]]:
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT key, value, version, updated_at, source, confidence, metadata FROM memory_store WHERE scope = ?", (scope.value,))
        rows = cur.fetchall()
        conn.close()

        result = {}
        for row in rows:
            result[row["key"]] = {
                "value": json.loads(row["value"]),
                "version": row["version"],
                "updated_at": row["updated_at"],
                "source": row["source"],
                "confidence": row["confidence"],
                "metadata": json.loads(row["metadata"])
            }
        return result

    # Legacy support
    def load(self, agent_id: str) -> Optional[AgentMemory]:
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT agent_id, interactions, metadata, last_updated FROM agent_memory WHERE agent_id = ?", (agent_id,))
        row = cur.fetchone()
        conn.close()
        if not row: return None
        return AgentMemory(
            agent_id=row["agent_id"],
            interactions=json.loads(row["interactions"]),
            metadata=json.loads(row["metadata"]),
            last_updated=datetime.fromisoformat(row["last_updated"]),
        )

    def save(self, memory: AgentMemory):
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO agent_memory (agent_id, interactions, metadata, last_updated)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(agent_id) DO UPDATE SET
            interactions=excluded.interactions,
            metadata=excluded.metadata,
            last_updated=excluded.last_updated
        """, (memory.agent_id, json.dumps(memory.interactions), json.dumps(memory.metadata), memory.last_updated.isoformat()))
        conn.commit()
        conn.close()
