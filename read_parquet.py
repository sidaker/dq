import pandas as pd
import numpy as np
pd.set_option('mode.chained_assignment', None)
dfin = pd.read_parquet("/Users/sbommireddy/Downloads/fsflights/")

print(dfin.head())
## filter voyage id with voyageid = '0000'
## change date format from YYYY-MM-DD to YYYY/MM/DD
### Check dep_port_country_md_code='GBR' and set to dep else arr.
print(dfin.columns)
## carrier,flight,direction,flight_date
## QR,0008,dep,2022/06/04
##flightdetails_carrier, voyage_number, flight_date

is_air =  dfin['voyage_number']!='0000'
dfin_air = dfin[is_air]
print(dfin.shape)
print(dfin_air.shape)

dfin_air['flight_date'] = pd.to_datetime(dfin_air['flight_date'])
dfin_air['flight_date'] = dfin_air['flight_date'].dt.strftime('%Y/%m/%d')


#print(dfin_air['flight_date'].head())
#print(dfin_air.dtypes)


print(dfin_air['flight_date'].head())
print(dfin_air['dep_port_country_md_code'].head(50))

# df['hasimage'] = np.where(df['photos']!= '[]', True, False)

# df.loc[df['A'] > 2, 'B'] = new_val
dfin_air["direction"] = np.where(dfin_air['dep_port_country_md_code']== 'GBR', 'dep', 'arr')


print(dfin_air['direction'].head())

dfin_air_final = dfin_air[['flightdetails_carrier','voyage_number','direction','flight_date']]

print(dfin_air_final.head())


## pwd write to CSV
dfin_air_final.to_csv('/Users/sbommireddy/Downloads/fsinput-full-schedules.csv')
