-- Drop the view if it already exists
DROP VIEW IF EXISTS member_latest_health_metrics;

-- Create view showing members with their most recent health metrics
CREATE VIEW member_latest_health_metrics AS
SELECT 
    u.user_id,
    u.first_name,
    u.last_name,
    u.email,
    m.date_of_birth,
    m.membership_status,
    hm.weight,
    hm.heart_rate,
    hm.height,
    hm.blood_pressure,
    hm.body_fat_percentage,
    hm.recorded_at as last_metric_date
FROM users u
JOIN member m ON u.user_id = m.user_id
LEFT JOIN LATERAL (
    SELECT weight, heart_rate, height, blood_pressure, body_fat_percentage, recorded_at
    FROM health_metric
    WHERE member_id = m.user_id
    ORDER BY recorded_at DESC
    LIMIT 1
) hm ON true;

-- View for members with user info
CREATE OR REPLACE VIEW member_view AS
SELECT 
    u.user_id,
    u.first_name,
    u.last_name,
    u.email,
    u.phone,
    u.created_at,
    m.date_of_birth,
    m.membership_status
FROM users u
JOIN member m ON u.user_id = m.user_id;

-- View for trainers with user info
CREATE OR REPLACE VIEW trainer_view AS
SELECT 
    u.user_id,
    u.first_name,
    u.last_name,
    u.email,
    u.phone,
    u.created_at,
    t.specialty,
    t.certification
FROM users u
JOIN trainer t ON u.user_id = t.user_id;

-- View for admins with user info
CREATE OR REPLACE VIEW admin_view AS
SELECT 
    u.user_id,
    u.first_name,
    u.last_name,
    u.email,
    u.phone,
    u.created_at,
    a.admin_role
FROM users u
JOIN admin a ON u.user_id = a.user_id;