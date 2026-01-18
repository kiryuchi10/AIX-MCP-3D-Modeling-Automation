-- 001_init.sql
-- MCP 3D Model Automation - Initial Schema
-- For MySQL 8.0+

CREATE DATABASE IF NOT EXISTS mcp3d
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'mcp3d_user'@'%' IDENTIFIED BY 'mcp3d_password';
GRANT ALL PRIVILEGES ON mcp3d.* TO 'mcp3d_user'@'%';
FLUSH PRIVILEGES;

USE mcp3d;

-- Jobs table: job status + parameters + artifact paths
CREATE TABLE IF NOT EXISTS jobs (
  id CHAR(36) PRIMARY KEY,
  status ENUM('QUEUED','RUNNING','SUCCEEDED','FAILED') NOT NULL DEFAULT 'QUEUED',
  input_type ENUM('IMAGE','MODEL_3D','LAYOUT_2D') NOT NULL,
  params_json JSON NULL,
  input_files_json JSON NULL,
  generated_script_path VARCHAR(512) NULL,
  output_files_json JSON NULL,
  logs_path VARCHAR(512) NULL,
  error_message TEXT NULL,
  run_time_sec INT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_jobs_status_created ON jobs(status, created_at);