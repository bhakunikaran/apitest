from flask import Flask, redirect, url_for, request
import psycopg2
import pandas
import numpy

def get_data():
	conn = psycopg2.connect("dbname='test1' user='postgres' password='KaranS@123' host='localhost' port='5432'")
	cur = conn.cursor()
	cur.execute("SELECT key,latitude,longitude FROM mapping")
	data = cur.fetchall()
	conn.commit()
	conn.close()
	data = pandas.DataFrame(numpy.column_stack(data))
	data = data.T
	data.columns=['key','latitude','longitude']
	return data

def get_all_points(latitude,longitude,radius):
	latitude = float(latitude) ; longitude = float(longitude)
	pincodes = []
	earth_radius = 6371 #used mean radius assuming earth is perfect sphere
	pi = 3.14159265358979
	angle_subtended = (float(radius)*360)/(2*pi*earth_radius)
	print(angle_subtended)
	data = get_data()
	for pincode,latitude_data,longitude_data in zip(data['key'],data['latitude'],data['longitude']):
		latitude_data = float(latitude_data) ; longitude_data = float(longitude_data)
		if abs(latitude_data - latitude) <= angle_subtended and abs(longitude_data - longitude) <= angle_subtended :
			pincodes.append(pincode)
		else:
			pass
	return pincodes

app = Flask(__name__)

@app.route('/get_using_self',methods = ['GET'])
def post_location():
	if request.method == 'GET':
		latitude = request.args.get('latitude')
		longitude = request.args.get('longitude')
		radius = request.args.get('radius')
		data = get_all_points(latitude,longitude,radius)
		return str(data)

if __name__ == '__main__':
	app.run(debug = True)
