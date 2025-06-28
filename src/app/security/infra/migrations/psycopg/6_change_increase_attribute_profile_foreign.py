from src.infra.migrator import model as migrator_model

migrator_script = """
ALTER TABLE tbl_profile ALTER COLUMN user_id TYPE VARCHAR(40);
"""

rollback_script = """
ALTER TABLE tbl_profile ALTER COLUMN user_id TYPE VARCHAR(25);
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
