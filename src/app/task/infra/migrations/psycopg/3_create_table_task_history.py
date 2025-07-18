from src.infra.migrator import model as migrator_model

migrator_script = """
CREATE TABLE IF NOT EXISTS tbl_history_task(
    id VARCHAR(25) PRIMARY KEY NOT NULL,
    task_id VARCHAR(40) NOT NULL,
    changed_at TIMESTAMP NOT NULL,
    type_of_change VARCHAR(25) NOT NULL,
    previous_values JSONB NULL,
    new_values JSONB NOT NULL,
    is_activated BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (task_id) REFERENCES tbl_task(id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""

rollback_script = """
DROP TABLE IF EXISTS tbl_history_task;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
