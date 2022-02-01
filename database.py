from sqlalchemy import create_engine
from conf import config


#a table for stocks (1 to many) connected to Expiration (1 to many) connected to Calls and Puts.

tables = {
    'Stocks': '''
        CREATE TABLE IF NOT EXISTS Stocks (
            ticker VARCHAR(10),
            PRIMARY KEY (ticker)
        );   
        ''',
        
    'Expirations': '''
        CREATE TABLE IF NOT EXISTS Expirations (
            ts TIMESTAMP,
            date DATE,
            ticker VARCHAR(10),
            PRIMARY KEY (ts, date, ticker),
            FOREIGN KEY (ticker) REFERENCES Stocks (ticker)
            );
    ''',
    
    'Calls': '''
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
    ''',
    'Puts': '''
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
            );''',
    'Prices': '''
        CREATE TABLE IF NOT EXISTS Prices (
            ticker VARCHAR(10),
            price FLOAT,
            ts TIMESTAMP,
            PRIMARY KEY (ts, price, ticker),
            FOREIGN key (ticker) REFERENCES Stocks(ticker)
        );   
        '''
}


def setup(cursor, reset = False):
    db_name = config['database']
    
    if reset:
        cursor.execute(f"DROP DATABASE {db_name}")
    try:    
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f'Created Database {db_name}')
    except:
        ...
        

    cursor.execute(f"USE {db_name};")
    for table_val in tables.values():
        cursor.execute(table_val)
        
    
    
def get_alchemy_engine(config):
    user = config['user']
    password = config['password']
    host = config['host']
    db_name = config['database']
    
    return create_engine(f'mysql+pymysql://{user}:{password}@{host}/{db_name}')