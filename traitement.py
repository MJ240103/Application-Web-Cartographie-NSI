#import modules
import folium

#afficher carte avec marqueur à partir de coordonnées
def aff_carte(lat,lon):
  m = folium.Map(location=[lat, lon])
  marqueur = folium.Marker([lat, lon],
                          color="red"
                          ).add_to(m)
  return m

#afficher carte avec marqueur à partir d'une liste de coordonnées
def aff_carte_liste(liste):
    m = folium.Map(location=[liste[0]["lat"], liste[0]["lon"]])
    for dico_coords in liste:
        folium.Marker([dico_coords["lat"], dico_coords["lon"]],color="red").add_to(m)
    return m

#créer liste avec trame
def trame_folium(trame):
  liste = trame.split(",")
  return liste


#calcul latitude à partir d'une trame en liste
def latD(liste):
    latD = 0
    if str(liste[3]) == "S":
        latD = -(round(float(liste[2][0:2])) + float(liste[2][2:])/60, 4)
    else:
        latD = round(float(liste[2][0:2]) + float(liste[2][2:])/60, 4)
  
    return latD


#calcul longitude à partir d'une trame en liste
def lonD(liste):
    lonD = 0
    if str(liste[5]) == "O":
        lonD = -(round(float(liste[4][0:2])) + float(liste[4][2:])/60, 4)
    else:
        lonD = round(float(liste[4][0:2]) + float(liste[4][2:])/60, 4)
    
    return lonD


#calcul latitude à partir d'une latitude et de la donnée Nord-Sud
def latE(lat, n_s):
    latD = 0
    if n_s == "S":
        latD = -(round(float(lat[0:2]) + float(lat[2:])/60, 4))
    else:
        latD = round(float(lat[0:2]) + float(lat[2:])/60, 4)
  
    return latD


#calcul longitude à partir d'une latitude et de la donnée Est-Ouest
def lonE(long, e_o):
    lonD = 0
    if e_o == "O":
        lonD = -(round(float(long[0:2]) + float(long[2:])/60, 4))
    else:
        lonD = round(float(long[0:2]) + float(long[2:])/60, 4)
    
    return lonD