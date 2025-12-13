import json
from typing import List, Optional
from .database import get_connection
from .models import WorkflowRun, WorkflowStepResult, AgentRecord


class WorkflowRepository:

    def create_run(self, workflow_name: str, status: str) -> int:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO workflow_runs (workflow_name, status) VALUES (?, ?)",
            (workflow_name, status),
        )

        run_id = cur.lastrowid
        conn.commit()
        conn.close()
        return run_id

    def save_step(self, step: WorkflowStepResult):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO workflow_steps
            (run_id, step_name, agent, status, output)
            VALUES (?, ?, ?, ?, ?)
            """,
            (step.run_id, step.step_name, step.agent, step.status, step.output),
        )

        conn.commit()
        conn.close()

    def update_run_status(self, run_id: int, status: str):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE workflow_runs SET status = ? WHERE id = ?",
            (status, run_id),
        )

        conn.commit()
        conn.close()


class AgentRepository:
    """Repository for persisting agent configurations."""

    def save_agent(self, agent: AgentRecord) -> int:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT OR REPLACE INTO agents
            (agent_id, agent_type, capabilities, config)
            VALUES (?, ?, ?, ?)
            """,
            (
                agent.agent_id,
                agent.agent_type,
                json.dumps(agent.capabilities),
                json.dumps(agent.config),
            ),
        )

        agent_db_id = cur.lastrowid
        conn.commit()
        conn.close()
        return agent_db_id

    def get_agent(self, agent_id: str) -> Optional[AgentRecord]:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM agents WHERE agent_id = ?", (agent_id,))
        row = cur.fetchone()
        conn.close()

        if row is None:
            return None

        return AgentRecord(
            agent_id=row["agent_id"],
            agent_type=row["agent_type"],
            capabilities=json.loads(row["capabilities"] or "[]"),
            config=json.loads(row["config"] or "{}"),
        )

    def list_agents(self) -> List[AgentRecord]:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM agents")
        rows = cur.fetchall()
        conn.close()

        return [
            AgentRecord(
                agent_id=row["agent_id"],
                agent_type=row["agent_type"],
                capabilities=json.loads(row["capabilities"] or "[]"),
                config=json.loads(row["config"] or "{}"),
            )
            for row in rows
        ]

    def delete_agent(self, agent_id: str) -> bool:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM agents WHERE agent_id = ?", (agent_id,))
        deleted = cur.rowcount > 0
        conn.commit()
        conn.close()
        return deleted
