#fonctions de base nécessaires
from flask import Flask, render_template, request
import folium
import random
from exif import Image
import os
from os.path import basename
from traitement import trame_folium, latD, lonD, aff_carte, latE, lonE, aff_carte_liste

#nom de l'application web
app_carto = Flask(__name__)

#route racine
@app_carto.route("/")
def index():
    #with open('static/jardin.jpg', 'rb') as image_file:
        #image_test = Image(image_file)
    
    #lat = image_test.gps_latitude
    #lon = image_test.gps_longitude
    #m = folium.Map(location = [(lat[0]+(lat[1]/60)+(lat[2]/3600)), (lon[0]+(lon[1]/60)+(lon[2]/3600))], zoom_start = 6)

    #image_page = "<img src='static/jardin.jpg' width='50'>"
    #popup = folium.Popup(image_page)
    #marker = folium.Marker([(lat[0]+(lat[1]/60)+(lat[2]/3600)), (lon[0]+(lon[1]/60)+(lon[2]/3600))], popup=popup).add_to(m)
    
    return render_template("index.html", horodateur=random.randint(1,10000))
    #return m._repr_html_()

@app_carto.route("/retour_carte", methods=["POST"])
def carte():
    #récup données
    lat = request.form["latitude"]
    lon = request.form["longitude"]
    trame = str(request.form["trame"])
    fichier = request.files["fichier"]
    image = request.files["image"]

    #affichage serveur
    print(f"Latitude = {lat} | Longitude = {lon}")
    print(f"Trame reçue = {trame}")
    print(f"Fichier reçu = {fichier.filename}")
    print(f"Image reçue = {image.filename}")

    #création map
    if trame != "":
        m = aff_carte(latD(trame_folium(trame)),lonD(trame_folium(trame)))
    elif lat != "" and lon != "":
        m = aff_carte(lat,lon)
    elif image.filename != "":
        image.save("static/" + image.filename)
        with open("static/" + str(image.filename), 'rb') as image_file:
            image_test = Image(image_file)

        if image_test.gps_latitude != None:
            lat = image_test.gps_latitude
            lon = image_test.gps_longitude
            m = folium.Map(location = [(lat[0]+(lat[1]/60)+(lat[2]/3600)), (lon[0]+(lon[1]/60)+(lon[2]/3600))], zoom_start = 6)

            image_page = "<img src='static/"+image.filename+"' width='100'>"
            popup = folium.Popup(image_page)
            marker = folium.Marker([(lat[0]+(lat[1]/60)+(lat[2]/3600)), (lon[0]+(lon[1]/60)+(lon[2]/3600))], popup=popup).add_to(m)
        else:
            m = aff_carte(10.303725,-109.217936)
            marker = folium.Marker([10.303725,-109.217936], popup = "La photo ne possède pas de coordonnées GPS !").add_to(m)
    else:
        fichier.save("static/" + fichier.filename)
        with open ("static/" + str(fichier.filename)) as fic:
            coords = []
            for ligne in fic:
                if ligne[3:6] == "GGA":
                    trame = ligne.split(",")
                    if trame[2] and trame[3] != "":
                        if trame[4] and trame[5]:
                            coords.append({"lat":latE(trame[2],trame[3]), "lon":lonE(trame[4],trame[5])})
        m = aff_carte_liste(coords)
    
    return m._repr_html_()

#écoute de l'application sur le port 8080
app_carto.run(host="0.0.0.0", port = 8080)