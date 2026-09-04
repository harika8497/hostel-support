-- Run this once in MySQL Workbench, or via the MySQL extension in VS Code,
-- or with: mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS hostel_support;
USE hostel_support;

CREATE TABLE IF NOT EXISTS reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    passcode VARCHAR(12) UNIQUE NOT NULL,
    mode ENUM('vent', 'resolve') NOT NULL DEFAULT 'vent',
    message TEXT NOT NULL,
    name VARCHAR(100),
    branch VARCHAR(100),
    year VARCHAR(20),
    hostel_block VARCHAR(50),
    flagged BOOLEAN DEFAULT FALSE,
    status ENUM('pending', 'in_progress', 'resolved') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS replies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_id INT NOT NULL,
    sender ENUM('student', 'staff') NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
);

SHOW TABLES;

SELECT * FROM reports;

-- Optional: a couple of sample rows so the dashboard isn't empty on first run
INSERT INTO reports (passcode, mode, message, flagged, status)
VALUES
('DEMO0001', 'vent', 'Sample entry: someone in my block keeps mocking my accent in front of others.', FALSE, 'pending'),
('DEMO0002', 'resolve', 'Sample entry: a senior has been taking my food money every week since orientation.', FALSE, 'pending');
