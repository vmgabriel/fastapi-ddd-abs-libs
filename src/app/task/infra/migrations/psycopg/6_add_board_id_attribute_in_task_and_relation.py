from src.infra.migrator import model as migrator_model

migrator_script = """
ALTER TABLE tbl_task ADD COLUMN IF NOT EXISTS board_id VARCHAR(40);

ALTER TABLE tbl_task
ADD CONSTRAINT fk_board
FOREIGN KEY (board_id) REFERENCES tbl_board(id)
ON UPDATE CASCADE ON DELETE CASCADE;


ALTER TABLE tbl_task ALTER COLUMN board_id SET NOT NULL;
"""

rollback_script = """
ALTER TABLE tbl_task DROP CONSTRAINT IF EXISTS fk_board;

ALTER TABLE tbl_task
DROP COLUMN IF EXISTS board_id;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
