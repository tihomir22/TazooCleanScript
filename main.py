from difflib import get_close_matches
import json
text = "04/06/2023 19:20:00   and the place is in front of the Barcelona's University, in the Street Meléndez Valdés number 48.  The police and the Municipal Police were there for hours, without any solution. I have never seen a traffic stuck like that before (in more than 30 years).  Somebody from the Municipal Police told me they could not do anything about it because of a Law: the car is parked in one way street, but in that place there are many vehicles and pedestrian paths, so the police can not act. We can only call the. In the street 9 OctubreB. The car AC906KS"
palabras_mensaje = text.split()

with open('streets.json', 'r',encoding='utf-8') as file:
    streets = json.load(file)
streets_lower = [street.lower() for street in streets]

def buscar_similitudes(calle_buscada):
    palabras_calle = calle_buscada.lower()
    similitudes = get_close_matches(palabras_calle, streets_lower, n=5, cutoff=0.5)
    return similitudes


similitudes = buscar_similitudes("octubre")

if similitudes:
    print("Se encontraron similitudes en el texto:")
    for similitud in similitudes:
        print(similitud)
else:
    print("No se encontraron similitudes en el texto.")
#
# extracted_streets = detect_street_names(text)