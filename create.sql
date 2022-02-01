
CREATE TABLE IF NOT EXISTS Stocks (
    ticker VARCHAR(10),
    PRIMARY KEY (ticker)
);   

CREATE TABLE IF NOT EXISTS Expirations (
    ts TIMESTAMP,
    date DATE,
    ticker VARCHAR(10),
    PRIMARY KEY (ts, date, ticker),
    FOREIGN KEY (ticker) REFERENCES Stocks (ticker)
    );

CREATE TABLE IF NOT EXISTS Calls (
    id INT AUTO_INCREMENT,
    exp_date DATE,
    ts TIMESTAMP,
    ticker VARCHAR(10) NOT NULL,
    contractSymbol VARCHAR(50),
    lastTradeDate DATETIME,
    strike FLOAT,
    lastPrice FLOAT,
    bid FLOAT,
    ask FLOAT,
    _change FLOAT,
    percentChange FLOAT,
    volume INT,
    openInterest INT,
    impliedVolatility FLOAT,
    inTheMoney TINYINT(1),
    contractSize VARCHAR(50),
    currency VARCHAR(10),
    PRIMARY KEY (id),
    FOREIGN KEY (ts, exp_date, ticker) REFERENCES Expirations (ts, date, ticker)
    );

CREATE TABLE IF NOT EXISTS Puts (
    id INT AUTO_INCREMENT,
    exp_date DATE,
    ts TIMESTAMP,
    ticker VARCHAR(10) NOT NULL,
    contractSymbol VARCHAR(50),
    lastTradeDate DATETIME,
    strike FLOAT,
    lastPrice FLOAT,
    bid FLOAT,
    ask FLOAT,
    _change FLOAT,
    percentChange FLOAT,
    volume INT,
    openInterest INT,
    impliedVolatility FLOAT,
    inTheMoney TINYINT(1),
    contractSize VARCHAR(50),
    currency VARCHAR(10),
    PRIMARY KEY (id),
    FOREIGN KEY (ts, exp_date, ticker) REFERENCES Expirations (ts, date, ticker)
    );

CREATE TABLE IF NOT EXISTS Prices (
    ticker VARCHAR(10),
    price FLOAT,
    ts TIMESTAMP,
    PRIMARY KEY (ts, price, ticker),
    FOREIGN key (ticker) REFERENCES Stocks(ticker)
);   
