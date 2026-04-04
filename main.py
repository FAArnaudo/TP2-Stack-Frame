import requests
import ctypes

# Cargamos la libreria 
lib_converter = ctypes.CDLL('./to_int_plus_one.so')

# Definimos los tipos de los argumentos de la función factorial
lib_converter.to_int_plus_one.argtypes = (ctypes.c_float,)

# Definimos el tipo del retorno de la función factorial
lib_converter.to_int_plus_one.restype = ctypes.c_int

# Creamos nuestra función factorial en Python
# hace de Wrapper para llamar a la función de C
def float_to_int_plus_one(num):
    return  lib_converter.to_int_plus_one(num)


flag = True

print("gini>> Este es un programa para obtener los valores, de un cierto pais, del indice GINI\n")

while(flag):
    country = input("gini>> Ingrese un pais: ")

    URL = f"https://api.worldbank.org/v2/country/{country}/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=1000"

    response = requests.get(URL)
    values = response.json()[1]

    #for data in values:
    #    print(f"{data}\n")

    for item in values:
        if item["value"] == None:
            continue
        print(f"date: {item['date']}, value: {item['value']}\n")
        int_converted = float_to_int_plus_one(item["value"])
        print(f"date: {item['date']}, value: {int_converted}\n")

    flag = input("Continuar --> 1\nFinalizar --> 0\n")
    if flag == False:
        break


print("Programa finalizado.")
