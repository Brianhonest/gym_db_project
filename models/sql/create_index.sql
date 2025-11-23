-- Index on email for user login lookups (very common operation)
CREATE INDEX idx_users_email ON users(email);

-- Index on member_id in health_metric for dashboard queries
CREATE INDEX idx_health_metric_member_recorded ON health_metric(member_id, recorded_at DESC);

-- Index on class_id in class_registration for checking class capacity
CREATE INDEX idx_class_registration_class_id ON class_registration(class_id);