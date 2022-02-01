import yfinance as yf
from datetime import datetime
from pymysql import connect
from conf import config
from database import setup, get_alchemy_engine
from utils import enhance_df
from argparse import ArgumentParser
from date import market_open
from time import sleep
from collections import namedtuple

def main(reset):

    with connect(**config, autocommit = True) as conn:
        with conn.cursor() as cursor:
            setup(cursor, reset)
            alchemy_engine = get_alchemy_engine(config)
            
            while True:
                if market_open():
                    print('Market Open - Grabbing Data')
                    
                    cursor.execute("SELECT * FROM Stocks")
                    
                    #each row is an array of fields, but tickers only has one field
                    tickers = [i[0] for i in cursor.fetchall()]
                    
                    for t in tickers:
                        print(f'\n\nScraping {t}...')
                        try:
                            tick = yf.Ticker(t)
                            price = tick.history(period='1d')['Close'][0]
                            exps = tick.options
                            
                        except:
                            print(f'Invalid ticker: {t}')
                            continue
                            
                        ts = str(datetime.now())
                        cursor.execute(f"INSERT INTO Prices (ticker, price, ts) VALUES ('{t}', '{price}', '{ts}')")
                        
                        for dt in exps:
                            print(f'\tGrabbing expiration: {dt}')
                            
                            try:
                                options = tick.option_chain(dt)
                            except:
                                if not tick._expirations:
                                    tick._download_options()
                                options = tick._download_options(tick._expirations[dt])
                                if not options:
                                    continue
                                options = dict(options)
            
                                options = namedtuple('Options', ['calls', 'puts'])(**{
                                    "calls": tick._options2df(options['calls']),
                                    "puts": tick._options2df(options['puts'])
                                })
                                
                            puts, calls = options.puts, options.calls
                            calls = enhance_df(calls, t, ts, dt)
                            puts = enhance_df(puts, t, ts, dt)
                            
                            cursor.execute(f"INSERT INTO Expirations (ts, date, ticker) VALUES ('{ts}', '{dt}', '{t}');")
                            calls.to_sql('calls', alchemy_engine, if_exists = 'append', index = False)
                            puts.to_sql('puts', alchemy_engine, if_exists = 'append', index = False)
                            print(calls.head())
                            print(puts.head())    
                                                        
                else:
                    print('Market Closed, checking again in 1 hr...')
                            
                #pause 1 hour
                sleep(60 * 60)
        
    
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('reset', default = False, type = bool, nargs = '?')
    args = parser.parse_args()
    main(args.reset)