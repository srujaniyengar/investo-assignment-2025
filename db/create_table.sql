-- Create the ticker_data table if it doesn't exist
CREATE TABLE IF NOT EXISTS ticker_data (
    datetime TIMESTAMP PRIMARY KEY,
    open DECIMAL(10, 5),
    high DECIMAL(10, 5),
    low DECIMAL(10, 5),
    close DECIMAL(10, 5),
    volume INTEGER,
    instrument TEXT
);