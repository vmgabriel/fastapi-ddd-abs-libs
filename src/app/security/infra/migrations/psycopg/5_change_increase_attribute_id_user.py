from src.infra.migrator import model as migrator_model

migrator_script = """
ALTER TABLE tbl_user 
    ALTER COLUMN id TYPE VARCHAR(40),ALTER COLUMN id SET NOT NULL;
"""

rollback_script = """
ALTER TABLE tbl_user 
    ALTER COLUMN id TYPE VARCHAR(25),ALTER COLUMN id SET NOT NULL,ADD PRIMARY KEY (id);
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
