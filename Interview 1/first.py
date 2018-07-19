from flask import Flask, redirect, url_for, request
import pandas, psycopg2
import numpy

def add_to_data(pincode,address,city,latitude,longitude):
	conn = psycopg2.connect("dbname='test1' user='postgres' password='KaranS@123' host='localhost' port='5432'")
	cur = conn.cursor()
	cur.execute("INSERT INTO mapping VALUES(%s,%s,%s,%s,%s,%s)", (pincode,address,city,latitude,longitude,'NaN'))
	conn.commit()
	conn.close()

def add_data(pincode,address,city,latitude,longitude):
	around_diff = 0.00005
	conn = psycopg2.connect("dbname='test1' user='postgres' password='KaranS@123' host='localhost' port='5432'")
	cur = conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS mapping(key varchar PRIMARY KEY NOT NULL, place_name varchar, admin_name1 varchar, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, accuracy varchar)")
	conn.commit()
	cur.execute("SELECT * FROM mapping")
	data = cur.fetchall()
	conn.commit()
	conn.close()
	data = pandas.DataFrame(numpy.column_stack(data))
	data = data.T
	data.columns = ['key', 'place_name', 'admin_name1','latitude','longitude','accuracy']
	for key in data['key']:
		if pincode in key:
			return False
		else :
			pass
	for data_latitude in data["latitude"]:
		diff = abs(float(latitude) - float(data_latitude))
		if diff <= around_diff:
			return False
		else :
			pass
	for data_longitude in data["longitude"]:
		diff = abs(float(longitude) - float(data_longitude))
		if diff < around_diff:
			return False
		else :
			pass
	add_to_data(pincode,address,city,latitude,longitude)
	return True

app = Flask(__name__)

@app.route('/post_location',methods = ['POST'])
def post_location():
	if request.method == 'POST':
		pincode = request.form['pincode']
		address = request.form['address']
		city = request.form['city']
		latitude = request.form['latitude']
		longitude = request.form['longitude']
		result = add_data(pincode,address,city,latitude,longitude)
		if result :
			return 'Data Added successfully'
		else:
			return "data already present"

if __name__ == '__main__':
	app.run(debug = True)
