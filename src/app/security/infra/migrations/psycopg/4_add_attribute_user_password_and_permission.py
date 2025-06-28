from src.infra.migrator import model as migrator_model

migrator_script = """
ALTER TABLE tbl_user 
ADD COLUMN permissions VARCHAR(250) NOT NULL DEFAULT '';
    
ALTER TABLE tbl_user 
ADD COLUMN password VARCHAR(250) NOT NULL;
"""

rollback_script = """
ALTER TABLE tbl_user 
DROP COLUMN permissions;
    
ALTER TABLE tbl_user 
DROP COLUMN password;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
