-- 003_paper2code_schema.sql
-- Paper2Code integration schema additions

USE mcp3d;

-- Papers table
CREATE TABLE IF NOT EXISTS papers (
  id CHAR(36) PRIMARY KEY,
  title VARCHAR(512) NOT NULL,
  authors_json JSON NULL,
  abstract TEXT NULL,
  doi VARCHAR(256) NULL,
  arxiv_id VARCHAR(64) NULL,
  url VARCHAR(512) NULL,
  source VARCHAR(64) NULL,
  pdf_path VARCHAR(512) NULL,
  metadata_json JSON NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_papers_doi (doi),
  INDEX idx_papers_arxiv (arxiv_id)
);

-- Paper extractions table (Paper2Code output)
CREATE TABLE IF NOT EXISTS paper_extractions (
  id CHAR(36) PRIMARY KEY,
  paper_id CHAR(36) NOT NULL,
  job_id CHAR(36) NULL,
  status ENUM('PENDING','RUNNING','DONE','FAILED') NOT NULL DEFAULT 'PENDING',
  summary TEXT NULL,
  algorithms_json JSON NULL,
  code_blocks_json JSON NULL,
  theory_json JSON NULL,
  project_plan_json JSON NULL,
  artifacts_path VARCHAR(512) NULL,
  error_message TEXT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE,
  FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE SET NULL,
  INDEX idx_extractions_paper_id (paper_id),
  INDEX idx_extractions_job_id (job_id),
  INDEX idx_extractions_status (status)
);

-- Collections table
CREATE TABLE IF NOT EXISTS collections (
  id CHAR(36) PRIMARY KEY,
  name VARCHAR(256) NOT NULL,
  description TEXT NULL,
  papers_json JSON NULL,
  metadata_json JSON NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_collections_name (name)
);