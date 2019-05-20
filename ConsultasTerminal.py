
import requests
from lxml import etree
import os

key="200468450-2feacdf11dc31b50eff73d71b8599e97"
mapboxkey="pk.eyJ1IjoibHVpc2FvIiwiYSI6ImNqdmdkYzR5YjA1cHY0OW5vc2syOHR1Z3oifQ.TlhTDvGuB9-JJr_Vyj49zA"
yandexkey="trnsl.1.1.20190515T102841Z.48d3d2036e46a0f2.0f94d2311312265104e71b5ddc061cc1370ed213"


lugar=str(input("Dime una ciudad:	")).replace(" ","%20")

pais=str(input("Dime el país:	"))
yandex={"key":yandexkey,"text":pais,"lang":"es-en"}

traduccion=requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate',params=yandex)
pais=traduccion.json()["text"][0]
link=str("https://api.mapbox.com/geocoding/v5/mapbox.places/"+lugar+".json")

mapbox={"access_token":mapboxkey}

r=requests.get(link,params=mapbox)
print(r.url)
input()
if r.status_code == 200:
	doc=r.json()
	for lugares in doc["features"]:
		for regiones in lugares["context"]:
			if regiones["id"].find("country")!=-1 and regiones["text"]==pais:
				print(lugares["place_name"])
				lat=str(lugares["center"][1])
				lon=str(lugares["center"][0])
				print("Longitud: ",lugares["center"][0])
				print("Latitud: ",lugares["center"][1])


Dis=input("Dime un radio en kilómetros:	")
Dis=str(float(Dis)/1.609)
mountainproject={"lat":lat,"lon":lon,"maxDistance":Dis,"key":key}

r=requests.get('https://www.mountainproject.com/data/get-routes-for-lat-lon',params=mountainproject)
if r.status_code == 200:
	doc=r.json()
	for p in doc["routes"]:
		print (p["name"],"-",p["type"],"-	Latitud:",p["latitude"],", Longitud:",p["longitude"])
		print()