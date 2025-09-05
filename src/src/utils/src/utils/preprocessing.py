import pandas as pd

def merge_yields_inflation(yields, wb, country_code, country_name):
    """
    Une yields de 10Y con inflación anual para un país dado.
    
    Parámetros:
    - yields: DataFrame con columnas 'Year' y código del país (ej. 'US10')
    - wb: DataFrame con columnas 'Country', 'Year', 'inflation_yoy'
    - country_code: código de 10Y en yields (ej. 'US10')
    - country_name: nombre del país en wb (ej. 'United States')
    
    Devuelve:
    - DataFrame con columnas ['yield_10y', 'inflation_yoy']
    """
    y = yields[['Year', country_code]].rename(columns={country_code:'yield_10y'})
    i = wb.query("Country == @country_name")[['Year','inflation_yoy']]
    df = (y.merge(i, on='Year', how='inner')
            .dropna()
            .set_index('Year')
            .sort_index())
    return df
