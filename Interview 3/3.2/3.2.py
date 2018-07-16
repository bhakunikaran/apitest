from flask import Flask, redirect, url_for, request
import psycopg2
import json,pandas,numpy
from shapely.geometry import Point, Polygon

def prepare_data():
	data_json = {}
	conn = psycopg2.connect("dbname='test1' user='postgres' password='KaranS@123' host='localhost' port='5432'")
	cur = conn.cursor()
	cur.execute("SELECT * FROM cities")
	data = cur.fetchall()
	conn.commit()
	conn.close()
	data = pandas.DataFrame(numpy.column_stack(data))
	data = data.T
	data.columns=['name','latitude','longitude']
	names = set()
	names = [x for x in data['name'] if not (x in names or names.add(x))]
	for name in names:
		data_json[name] = []
	for name,latitude,longitude in zip(data['name'],data['latitude'],data['longitude']):
		latitude = float(latitude); longitude = float(longitude)
		data_json[name].append((latitude,longitude))
	return data_json

def find(latitude,longitude):
	data_json = prepare_data()
	point = Point(float(latitude),float(longitude))
	for city_name in data_json:
		city_coords = data_json[city_name]
		city_shape = Polygon(city_coords)
		if point.within(city_shape):
			return city_name
		else:
			pass
	return "The location you inserted is out from out locations present in our database"


app = Flask(__name__)

@app.route('/find_location',methods = ['POST'])
def post_location():
	if request.method == 'POST':
		latitude = request.form['latitude']
		longitude = request.form['longitude']
		city = find(latitude,longitude)
		return city

if __name__ == '__main__':
	app.run(debug = True)
