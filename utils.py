
def enhance_df(df, t, ts, dt):
    df['ticker'] = t
    df['ts'] = ts
    df['exp_date'] = dt

    #change is sql keyword
    df.rename(columns = {'change':'_change'}, inplace = True)
    return df
