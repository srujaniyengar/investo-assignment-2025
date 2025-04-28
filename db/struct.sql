CREATE TABLE IF NOT EXISTS stock_data (
    datetime TIMESTAMP PRIMARY KEY,
    open DECIMAL(10, 5),
    high DECIMAL(10, 5),
    low DECIMAL(10, 5),
    close DECIMAL(10, 5),
    volume INTEGER
);