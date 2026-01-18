-- 002_seed.sql
-- Development seed data (optional)

USE mcp3d;

INSERT INTO jobs (id, status, input_type, params_json, input_files_json)
VALUES (
  '00000000-0000-0000-0000-000000000001',
  'SUCCEEDED',
  'IMAGE',
  JSON_OBJECT('target_width_mm', 100, 'reference_type', 'bounding_box'),
  JSON_ARRAY('/data/uploads/demo.png')
)
ON DUPLICATE KEY UPDATE id=id;