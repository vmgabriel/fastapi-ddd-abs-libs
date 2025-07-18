from src.infra.migrator import model as migrator_model

migrator_script = """
CREATE TABLE IF NOT EXISTS tbl_ownership_board(
    id VARCHAR(25) PRIMARY KEY NOT NULL,
    board_id VARCHAR(40) NOT NULL,
    user_id VARCHAR(40) NOT NULL,
    is_activated BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (board_id) REFERENCES tbl_board(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES tbl_user(id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""

rollback_script = """
DROP TABLE IF EXISTS tbl_ownership_board;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
