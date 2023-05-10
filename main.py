import json
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from difflib import get_close_matches

text = "04/06/2023 05:58:00   the street Abu Masaifa A in front of boulevard de Waterloo is blocked.  this car (plate 533KAS) is stuck there since a lot time.  for more information, please call 093/21.47.86.  the police are doing something about this but they can't help us to move our cars from the street Abu Masaifa in front of Boulevard de Waterloo until the car plate 533KAS is moved.  The reason why we have a traffic jam in. In the street Abu Masaifa. The car AC696KS"
palabras_mensaje = text.split()

with open('streets.json', 'r', encoding='utf-8') as file:
    streets = json.load(file)
streets_lower = [street.lower() for street in streets]


def buscar_similitudes(palabra_buscada):
    similitudes = []
    similitudes_nltk = get_close_matches(palabra_buscada, streets_lower, n=1, cutoff=0.5)
    coincidencias = [street for street in streets_lower if palabra_buscada.lower() in street and palabra_buscada.lower() not in ['av','avenida','c/','calle','carrer','plaça','plaza','avinguda']]
    if len(coincidencias) > 0 and len(similitudes_nltk)>0:
        similitudes.append(coincidencias[0])
    return similitudes

def limpiar_palabra(palabra):
    # Aplicar transformaciones adicionales según tus necesidades
    if len(palabra) == 0:
        return palabra
    palabra_limpia = re.sub(r'\W+', '', palabra)  # Eliminar caracteres especiales
    split_by_uppercase = re.sub(r"([a-z])([A-Z])", r"\1 \2", palabra_limpia).split()
    if len(split_by_uppercase) > 0:
        palabra_limpia = split_by_uppercase[0] #Separar por mayusucla
    return palabra_limpia.lower()

def buscar_matricula(mensaje):
    regex_matricula = r'[A-Z]{1,3}\d{1,4}[A-Z]{0,3}'
    coincidencias = re.findall(regex_matricula, mensaje)
    return coincidencias

def buscar_calle(mensaje):
    palabras_texto = mensaje.split(" ")
    palabras_limpias = [limpiar_palabra(palabra_sucia) for palabra_sucia in palabras_texto]
    palabras_texto_filtradas = [palabra for palabra in palabras_limpias if len(palabra) > 3 ]
    detected_streets = []

    for word in palabras_texto_filtradas:
        similitudes = buscar_similitudes(word)
        if len(similitudes) > 0:
            detected_streets = detected_streets + similitudes
    return detected_streets

def analizar_sentimiento(mensaje):
    sia = SentimentIntensityAnalyzer()
    polaridad = sia.polarity_scores(mensaje)['compound']
    return polaridad

def extraer_adjetivos(texto):
    palabras = nltk.word_tokenize(texto)
    palabras_etiquetadas = nltk.pos_tag(palabras)
    adjetivos = [palabra[0] for palabra in palabras_etiquetadas if palabra[1] == 'JJ']
    return adjetivos

nltk.download('vader_lexicon')
nltk.download('punkt')




    

detected_streets = list(set(buscar_calle(text)))
detected_license_plates = list(set(buscar_matricula(text)))
polaridad = analizar_sentimiento(text)
adjetivos = extraer_adjetivos(text)
print(detected_streets)
print(detected_license_plates)
print("Polaridad:", polaridad)
print(adjetivos)