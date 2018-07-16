from flask import Flask, redirect, url_for, request
import psycopg2
import json

def insert(cur,conn,name,latitude,longitude):
    cur.execute("INSERT INTO cities VALUES (%s,%s,%s)",(name,latitude,longitude))
    conn.commit()

def add_to_table(name,coords):
	latitudes = []
	longitudes = []
	for coord in coords:
		latitudes.append(coord[0])
	for coord in coords:
		longitudes.append(coord[1])
	conn = psycopg2.connect("dbname='test1' user='postgres' password='KaranS@123' host='localhost' port='5432'")
	cur = conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS cities(name varchar,latitude DOUBLE PRECISION, longitude DOUBLE PRECISION)")
	conn.commit()
	for latitude,longitude in zip(latitudes,longitudes):
		insert(cur,conn,name,latitude,longitude)
	conn.close()


app = Flask(__name__)

@app.route('/json_load',methods = ['POST'])
def post_location():
	if request.method == 'POST':
		json_raw = request.form['json']
		json_raw = json.loads(json_raw)
		for i in json_raw['features']:
			name = i['properties']['name']
			coords = i['geometry']['coordinates'][0]
			add_to_table(name,coords)
		return "data added successfully"

if __name__ == '__main__':
	app.run(debug = True)
