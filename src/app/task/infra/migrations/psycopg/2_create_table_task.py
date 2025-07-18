from src.infra.migrator import model as migrator_model

migrator_script = """
CREATE TABLE IF NOT EXISTS tbl_task(
    id VARCHAR(40) PRIMARY KEY NOT NULL,
    user_id VARCHAR(40) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(250) NOT NULL,
    status VARCHAR(25) NOT NULL,
    icon_url VARCHAR(100) NULL,
    is_activated BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES tbl_user(id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""

rollback_script = """
DROP TABLE IF EXISTS tbl_task;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
