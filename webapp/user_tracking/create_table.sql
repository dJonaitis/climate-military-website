CREATE TABLE PageView (
  session_id INT,
  page TEXT,
  time_spent INT, 
  start_time DATETIME
);
CREATE TABLE TransferYear (
  session_id INT,
  year_entered INT
);