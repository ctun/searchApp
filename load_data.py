import pandas as pd
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_string_dtype
from sqlalchemy import create_engine
import csv

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

df = pd.read_csv("AB_NYC_2019.csv")

def locateBadData(fn, colName, columnData ):
  result = []
  for n,val in enumerate(columnData):
      if isinstance(val,str):
          try:
               result += [(n, fn(val))]
          except:
               result += [(n, val)]
               print('bad entry in ', colName, ' at line ', n, val)
      else:
         result += [(n, val)]

  return result

# find which rows has bad entries, number_of_reviews should be all int
column = 'number_of_reviews'
reviews = locateBadData( lambda x: int(x), column, df[column])
todel = [ d[0] for d in reviews if type(d[1]) != int]
df['number_of_reviews'] = [r[1] for r in reviews]   # load with numbers

# find which rows has bad entries in latitude column, all should be float
column = 'latitude'
latitudes = locateBadData( lambda x: float(x), column, df[column])
todel += [ d[0] for d in latitudes if type(d[1]) != float]
df['latitude'] = [ r[1] for r in latitudes]

# find which rows has bad data in longitude column, all should be float
column = 'longitude'
longitudes = locateBadData( lambda x: float(x), column, df[column])
todel += [ d[0] for d in longitudes if type(d[1]) != float]
todel = sorted(list(set(todel)))

df['longitude'] = [ r[1] for r in longitudes]  # set vslues to floats

print('removing rows(s): ', todel)
df1 = df.drop(todel)  # remove the line with bad entries

convert = { 'latitude': 'float' , 'longitude': 'float64', 
            'price': 'int32',
            'minimum_nights': 'int32',
            'number_of_reviews': 'int32',
            'reviews_per_month': 'float32', 
            'calculated_host_listings_count': 'int32', 
            'availability_365': 'int32'
          }

engine = create_engine('postgresql://localhost:5432/coban')
df1 = df1.astype(convert)
df1.to_sql('nyc', engine)
