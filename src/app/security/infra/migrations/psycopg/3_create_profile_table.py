from src.infra.migrator import model as migrator_model

migrator_script = """
CREATE TABLE IF NOT EXISTS tbl_profile(
    id VARCHAR(100) PRIMARY KEY NOT NULL,
    phone VARCHAR(25) NOT NULL,
    icon_url VARCHAR(200) NULL,
    is_activated BOOLEAN NOT NULL DEFAULT TRUE,
    user_id VARCHAR(25) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES tbl_user(id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""

rollback_script = """
DROP TABLE IF EXISTS tbl_profile;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
