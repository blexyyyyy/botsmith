import sqlite3
import json
from datetime import datetime
from typing import Optional

from botsmith.core.memory.models import AgentMemory
from botsmith.persistence.database import get_connection


class AgentMemoryRepository:
    """
    SQLite-backed persistent agent memory store.
    """

    def __init__(self, db_path=None):
        self.db_path = db_path

    def init_schema(self):
        conn = get_connection(self.db_path)
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS agent_memory (
            agent_id TEXT PRIMARY KEY,
            interactions TEXT,
            metadata TEXT,
            last_updated TEXT
        )
        """)

        conn.commit()
        conn.close()

    def load(self, agent_id: str) -> Optional[AgentMemory]:
        conn = get_connection(self.db_path)
        cur = conn.cursor()

        cur.execute(
            "SELECT agent_id, interactions, metadata, last_updated FROM agent_memory WHERE agent_id = ?",
            (agent_id,)
        )

        row = cur.fetchone()
        conn.close()

        if not row:
            return None

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
        """, (
            memory.agent_id,
            json.dumps(memory.interactions),
            json.dumps(memory.metadata),
            memory.last_updated.isoformat(),
        ))

        conn.commit()
        conn.close()
