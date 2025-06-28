from src.infra.migrator import model as migrator_model

migrator_script = """
ALTER TABLE IF EXISTS tbl_profile
    RENAME TO tbl_user;
"""

rollback_script = """
ALTER TABLE IF EXISTS tbl_user
    RENAME TO tbl_profile;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
