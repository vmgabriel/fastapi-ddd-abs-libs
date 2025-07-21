from src.infra.migrator import model as migrator_model

migrator_script = """
ALTER TABLE tbl_ownership_board
ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'viewer';

ALTER TABLE tbl_ownership_board ALTER COLUMN role SET NOT NULL;
"""

rollback_script = """
ALTER TABLE tbl_ownership_board
DROP COLUMN IF EXISTS role;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
