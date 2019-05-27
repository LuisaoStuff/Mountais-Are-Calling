from flask import Flask, render_template,request,abort
import requests
app = Flask(__name__)	

@app.route('/',methods=["GET","POST"])
def inicio():
    return render_template("home.html")

@app.route('/busqueda',methods=["GET","POST"])
def busqueda():
    ciudad=request.form.get("ciudad")
    pais=request.form.get("pais")
    radio=request.form.get("radio")
    try:
        mountainkey="200468450-2feacdf11dc31b50eff73d71b8599e97"
        mapboxkey="pk.eyJ1IjoibHVpc2FvIiwiYSI6ImNqdmdkYzR5YjA1cHY0OW5vc2syOHR1Z3oifQ.TlhTDvGuB9-JJr_Vyj49zA"
        yandexkey="trnsl.1.1.20190515T102841Z.48d3d2036e46a0f2.0f94d2311312265104e71b5ddc061cc1370ed213"
        yandex={"key":yandexkey,"text":pais,"lang":"es-en"}
        traduccion=requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate',params=yandex)
        pais=traduccion.json()["text"][0]
        link=str("https://api.mapbox.com/geocoding/v5/mapbox.places/"+ciudad+".json")
        mapbox={"access_token":mapboxkey}

        r=requests.get(link,params=mapbox)
        if r.status_code == 200:
            doc=r.json()
            features=[]
            for lugares in doc["features"]:
                for regiones in lugares["context"]:
                    if regiones["id"].find("country")!=-1 and regiones["text"]==pais:
                        latitud=str(lugares["center"][1])
                        longitud=str(lugares["center"][0])

        radio=str(float(radio)/1.609)
        mountainproject={"lat":latitud,"lon":longitud,"maxDistance":radio,"key":mountainkey}
        r=requests.get('https://www.mountainproject.com/data/get-routes-for-lat-lon',params=mountainproject)
        if r.status_code == 200:
            doc=r.json()
            for p in doc["routes"]:
                lat=p["latitude"]
                lon=p["longitude"]
                lugar=p["name"]
                features.append({"type": "Feature","geometry": {"type": "Point","coordinates": [lon, lat]},"properties": {"title": lugar,"icon": "marker"}})
                { "type": "Feature", "properties": { "id": "ak16994521", "type": 2.3 }, "geometry": { "type": "Point", "coordinates": [ lon, lat, 0.0 ] } }


    except:
        abort(404)
    return render_template("busqueda.html",features=features,latitud=latitud,longitud=longitud,mapboxkey=mapboxkey,ciudad=ciudad)    

@app.route('/noticias',methods=["GET","POST"])
def noticias():
    return render_template('noticias.html')

@app.route('/busqueda/blablacar',methods=["GET","POST"])
def blablacar():
    destino=request.form.get("destino")
    origen=request.form.get("origen")
    blablakey='9abf62d532d04a59a54fcec065b7307d'
    listaviajes=[]
    try:
        opciones={"locale":"es_ES","accept":"application/json","fn":origen,"tn":destino,"_format":"json","cur":"EUR","sort":"trip_price","order":"asc","key":blablakey}
        rutas=requests.get('https://public-api.blablacar.com/api/v2/trips',params=opciones)
        if rutas.status_code == 200:
            doc=rutas.json()

            for viajes in doc["trips"]:
                ruta=[]
                precio=viajes["price_with_commission"]["value"]
                sitioslibres=viajes["seats_left"]
                sitiostotales=viajes["seats"]
                FechaSalida=viajes["departure_date"]
                CiudadQuedada=viajes["departure_place"]["city_name"]
                DireccionQuedada=viajes["departure_place"]["address"]

                ruta.append(precio)
                ruta.append(sitioslibres)
                ruta.append(sitiostotales)
                ruta.append(FechaSalida)
                ruta.append(DireccionQuedada)
                try:
                    MarcaCoche=str(viajes["car"]["make"]+" "+viajes["car"]["model"])
                    ruta.append(MarcaCoche)
                except:
                    ruta.append("???")

                ruta.append(viajes["links"]["_front"])
                listaviajes.append(ruta)
        numviajes=len(listaviajes)
    except:
        abort(404)
    return render_template("blablacar.html",numviajes=numviajes,listaviajes=listaviajes)

app.run(debug=True)
