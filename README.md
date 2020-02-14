# searchApp

Feb 13, 2020
given lat,long, searches the location within a given radius (meters)

It talks to Postgres database running on localhost set in function FindLoc in search.py
conn = psycopg2.connect("dbname=..., user=...")

schema is in cre_table.txt

json format to send to flask server:

echo $jstr500
{"latitude": "40.7306", "longitude": "-73.9352", "distance": "500", "query": "two bedroom"}

curl -H  "Content-Type: application/json"  --data  "$jstr500"  http://localhost:5000/search







