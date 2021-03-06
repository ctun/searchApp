from math import cos, sqrt
import psycopg2

circum = 40075160    # circumference at the equator
circum = 40075017
pi = 3.14159

north_south_circum = 40008000
north_south_circum = 39940653.0

class Location:
   def __init__(self,grp, hood, x,y):
       self.neighborhood_grp = grp
       self.neighborhood = hood
       self.lat = x
       self.long = y

def asRadians(degrees):
    return degrees * pi / 180

def getXYpos(p0, p):
    """ Calculates X and Y distances in meters.
    """
    deltaLatitude = p.lat - p0.lat
    deltaLongitude = p.long - p0.long
    latitudeCircumference = circum * cos(asRadians(p0.lat))
    resultX = deltaLongitude * latitudeCircumference / 360
    resultY = deltaLatitude * north_south_circum / 360.0
    return resultX, resultY

def inRadius(p, locations,r):
    found = []

    for local in locations:
        p1  = Location(None, None ,  local[1], local[2])
        dx,dy = getXYpos(p, p1)
        if sqrt((dx ** 2 + dy ** 2)) < r:
            found += [local]

    return found

def getLatLong(lat, dx,dy):
    dlat = dy * 360.0 / north_south_circum 
    latitudeCircumference = circum * cos( (pi / 180.0) * lat )
    dlong = dx * 360.0 / latitudeCircumference
    return dlat,dlong

def findLoc(p,r):
    # p    where you are
    # r    distance in meters

    # comput change in  lat amd long from r
    dlat, dlong = getLatLong(p.lat, r, r)

    sql = "SELECT id, latitude, longitude, neighbourhood_group, neighbourhood from nyc "
    where = "  where abs(latitude - %s) < %s and abs(longitude - %s) < %s"

    sql += where
    conn = psycopg2.connect("dbname=coban user=postgres")
    cur = conn.cursor()
    cur.execute(sql, (str(p.lat), str(dlat), str(p.long), str(dlong), ) )
    locations = cur.fetchall()    # no error checking here for now.

    result = []
    found = inRadius(p,locations, r)
    for loc in found:
       result += [{ 'id': loc[0],
                    'latitude': loc[1], 'longitude':loc[2], 
                    'neighbourhood_group':loc[3], 'neighbourhood':loc[4]
                  }]
    if conn:
       conn.close()

    return result

if __name__ == "__main__":
  r = 1132.90
  city = Location(None, None, 40.4998, -74.2408)
  foo = findLoc (city, r) 
  print (foo)
