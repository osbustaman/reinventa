import re

from geopy.distance import geodesic
from geopy.geocoders import Nominatim

def validarRut(rut):
    rut = rut.replace(".", "").replace("-", "")  # Eliminar puntos y guiones
    if not re.match(r'^\d{1,8}[0-9K]$', rut):  # Verificar formato
        return False
    rut_sin_dv = rut[:-1]
    dv = rut[-1].upper()  # Obtener dígito verificador
    multiplicador = 2
    suma = 0
    for r in reversed(rut_sin_dv):
        suma += int(r) * multiplicador
        multiplicador += 1
        if multiplicador == 8:
            multiplicador = 2
    resto = suma % 11
    dv_calculado = 11 - resto
    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(dv_calculado)
    return dv == dv_calculado


def getLatitudeLongitude(address):
        # Crear un objeto geolocator utilizando el proveedor Nominatim
        geolocator = Nominatim(user_agent="Nominatim", timeout=10)

        # Obtener la ubicación (latitud, longitud) a partir de la dirección
        location = geolocator.geocode(address)

        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        else:
            return None, None
        
def isWithinTheDiameter(lat_a, lon_a, lat_b, lon_b, radio_km = 0.1):
    # Crear objetos de ubicación para A y B
    location_a = (lat_a, lon_a)
    location_b = (lat_b, lon_b)

    # Calcular la distancia entre las ubicaciones A y B en kilómetros
    distance_km = geodesic(location_a, location_b).kilometers

    # Verificar si la distancia es menor o igual al radio deseado
    return distance_km <= radio_km