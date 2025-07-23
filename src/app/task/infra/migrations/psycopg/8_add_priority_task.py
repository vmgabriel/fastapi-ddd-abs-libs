from src.infra.migrator import model as migrator_model

migrator_script = """
ALTER TABLE tbl_task
ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'low';

ALTER TABLE tbl_task ALTER COLUMN priority SET NOT NULL;
"""

rollback_script = """
ALTER TABLE tbl_task
DROP COLUMN IF EXISTS priority;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
