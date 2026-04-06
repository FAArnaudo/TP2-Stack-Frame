import requests
import ctypes
import matplotlib.pyplot as plt
from pathlib import Path

# Cargamos la libreria
LIB_PATH = Path(__file__).resolve().parent / "build" / "to_int_plus_one.so"
lib_converter = ctypes.CDLL(str(LIB_PATH))

# Definimos los tipos de los argumentos de la función de conversión
lib_converter.to_int_plus_one.argtypes = (ctypes.c_float,)

# Definimos el tipo del retorno de la función de conversión
lib_converter.to_int_plus_one.restype = ctypes.c_int


# Creamos nuestra función de conversión en Python
# hace de Wrapper para llamar a la función de C
def float_to_int_plus_one(num):
    return lib_converter.to_int_plus_one(num)


def print_results_table(results):
    headers: tuple[str, str, str] = ("Fecha", "Valor original", "Valor convertido")
    rows: list[tuple[str, str, str]] = [headers]

    for result in results:
        rows.append(
            (
                str(result["date"]),
                str(result["value"]),
                str(result["converted_value"]),
            )
        )

    widths = [max(len(row[index]) for row in rows) for index in range(len(headers))]
    separator = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    print(separator)
    print(
        "| "
        + " | ".join(
            headers[index].ljust(widths[index]) for index in range(len(headers))
        )
        + " |"
    )
    print(separator)

    for row in rows[1:]:
        print(
            "| "
            + " | ".join(row[index].ljust(widths[index]) for index in range(len(row)))
            + " |"
        )

    print(separator)
    print()


flag = True

print(
    "gini>> Este es un programa para obtener los valores de un codigo de pais del indice GINI (ej: ar, arg)\n"
)

while flag:
    country = input("gini>> Ingrese un codigo de pais (ej: ar o arg): ")

    URL = f"https://api.worldbank.org/v2/country/{country}/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=1000"

    try:
        # Hacemos la consulta a la API del Banco Mundial con un timeout de 10 segundos
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        print("gini>> No se pudo consultar la API del Banco Mundial.\n")
        flag = input("Continuar --> 1\nFinalizar --> 0\n").strip() == "1"
        continue
    except ValueError:
        print("gini>> La API devolvio una respuesta invalida.\n")
        flag = input("Continuar --> 1\nFinalizar --> 0\n").strip() == "1"
        continue

    if (
        isinstance(data, list)
        and data
        and isinstance(data[0], dict)
        and "message" in data[0]
    ):
        print("gini>> El codigo de pais ingresado es invalido.\n")
        flag = input("Continuar --> 1\nFinalizar --> 0\n").strip() == "1"
        continue

    if len(data) < 2 or not isinstance(data[1], list):
        print("gini>> No se encontraron datos para el codigo de pais ingresado.\n")
        flag = input("Continuar --> 1\nFinalizar --> 0\n").strip() == "1"
        continue

    values = data[1]
    found_values = False
    results = []
    years = []
    gini_values = []

    # Procesamos los valores obtenidos de la API, filtrando los que
    # no tienen valor y aplicando la conversión a los que si lo tienen
    for item in values:
        if item["value"] is None:
            continue
        found_values = True
        years.append(int(item["date"]))
        gini_values.append(item["value"])

        # Convertimos el valor a entero usando la función de conversión en C
        int_converted = float_to_int_plus_one(item["value"])
        results.append(
            {
                "date": item["date"],
                "value": item["value"],
                "converted_value": int_converted,
            }
        )

    if found_values:
        print_results_table(results)

        combined = sorted(zip(years, gini_values))
        years_sorted, values_sorted = zip(*combined)

        plt.figure()
        plt.plot(years_sorted, values_sorted)
        plt.xlabel("Año")
        plt.ylabel("Índice GINI")
        plt.title(f"Índice GINI - {country.upper()}")
        plt.grid()
        plt.show()

    if not found_values:
        print(
            "gini>> El codigo de pais ingresado no tiene valores GINI disponibles en ese rango.\n"
        )

    flag = input("Continuar --> 1\nFinalizar --> 0\n").strip() == "1"


print("Programa finalizado.")
