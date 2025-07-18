from src.infra.migrator import model as migrator_model

migrator_script = """
CREATE TABLE IF NOT EXISTS tbl_board(
    id VARCHAR(40) PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(250) NOT NULL,
    icon_url VARCHAR(100) NULL,
    is_activated BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP NULL
);
"""

rollback_script = """
DROP TABLE IF EXISTS tbl_board;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
