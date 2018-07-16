import psycopg2
import csv
import pandas
file = pandas.read_csv('IN.csv')
def connection():
    conn = psycopg2.connect("dbname='test1' user='postgres' password='KaranS@123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE mapping(key varchar PRIMARY KEY NOT NULL, place_name varchar, admin_name1 varchar, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, accuracy varchar)")
    print("Records created successfully")
    return cur,conn
def insert(cur,conn,key_pk,placename_pk,admin_name1_pk,latitude,longitude,accuracy):
    cur.execute("INSERT INTO mapping VALUES (%s,%s,%s,%s,%s,%s)",(key_pk,placename_pk,admin_name1_pk,latitude,longitude,accuracy))
    conn.commit()
cur,conn = connection()
for key_pk,placename_pk,admin_name1_pk,latitude,longitude,accuracy in zip(file['key'],file['place_name'],file['admin_name1'],file['latitude'],file["longitude"],file['accuracy']):
	print('inserting ' + key_pk + ' ' + placename_pk + ' ' + str(admin_name1_pk) + ' ' + str(latitude) +  ' ' + str(longitude) +' ' + str(accuracy))
	if accuracy == 'Nan':
		insert(cur,conn,key_pk,placename_pk,admin_name1_pk,latitude,longitude,0)
	else:
		insert(cur,conn,key_pk,placename_pk,admin_name1_pk,latitude,longitude,accuracy)
conn.close()
