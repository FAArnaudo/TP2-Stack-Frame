# TP2-Stack-Frame
Este es el repositorio del trabajo práctico N° 2 de la materia de Sistemas de Computación.

## Grupo
- *Ataque x86*

## Integrantes
- *Arnaudo, Federico Andres*
- *Perotti, Franco José*

# Script de Python - main.py

Este programa en Python consulta la API del Banco Mundial para obtener valores del índice GINI de un país ingresado por el usuario (entre 2011 y 2020). 

Luego, utiliza la librería `ctypes` para cargar una biblioteca compartida escrita en C (`to_int_plus_one.so`) y llamar a una función que convierte cada valor flotante en entero y le suma uno. 

Finalmente, muestra tanto el valor original como el valor transformado, repitiendo el proceso hasta que el usuario decida finalizar.

## Diagramas del sistema

### 1. Diagrama de bloques

```mermaid
flowchart LR
    A[Usuario] --> B[main.py]
    B --> C[API Banco Mundial]
    B --> D[ctypes]
    D --> E[to_int_plus_one.so]
    E --> F[converter.c]
    F --> G[to_int.s]
    F --> H[plus_one.s]
    G --> F
    H --> F
    F --> B
    B --> I[Salida por pantalla]
```


### 2. Flujo general

```mermaid
flowchart TD
    A[Usuario ingresa un país] --> B[main.py]
    B --> C[Consulta a la API del Banco Mundial]
    C --> D[Respuesta JSON con valores GINI]
    D --> E[main.py filtra valores no nulos]
    E --> F[ctypes carga to_int_plus_one.so]
    F --> G[converter.c: to_int_plus_one]
    G --> H[to_int.s convierte float a int]
    H --> I[plus_one.s suma 1]
    I --> J[converter.c devuelve el entero transformado]
    J --> K[main.py imprime valor original y valor transformado]
    K --> L{Continuar?}
    L -->|Sí| A
    L -->|No| M[Fin del programa]
```

### 3. Diagrama de secuencia

```mermaid
sequenceDiagram
    actor U as Usuario
    participant P as main.py
    participant WB as API Banco Mundial
    participant CT as ctypes
    participant C as converter.c
    participant T as to_int.s
    participant A as plus_one.s

    U->>P: Ingresa pais
    P->>WB: GET índice GINI 2011:2020
    WB-->>P: JSON con valores
    loop Por cada valor no nulo
        P->>CT: float_to_int_plus_one(valor)
        CT->>C: to_int_plus_one(float)
        C->>T: to_int(..., a)
        T-->>C: int truncado
        C->>A: plus_one(..., a)
        A-->>C: int + 1
        C-->>CT: resultado entero
        CT-->>P: resultado entero
        P-->>U: Muestra valor original y transformado
    end
    P-->>U: Pregunta si desea continuar
```

# Comandos utilizados:

```gcc -shared -o to_int_plus_one.so converter.o to_int.o plus_one.o```

Usa el compilador GCC (GNU Compiler Collection) para crear una biblioteca compartida.

- -shared: Esto crea un fichero shared object llamado **to_int_plus_one.so**.
- -o: Define el nombre del archivo .so de salida.

Enlaza los objetos generados y produce la librería compartida (.so) llamada **to_int_plus_one.so**, que luego puede ser usada por el programa **main.py**.

```python3 ./main.py```

Para ejecutar el script de Python.


## Convención de llamada

```as --64 -g -o to_int.o to_int.s```

```as --64 -g -o plus_one.o plus_one.s```

```gcc -g -O0 -c -o converter.o converter.c```

```gcc -shared -o to_int_plus_one.so converter.o to_int.o plus_one.o```

## GDB

Iniciar la ejecución con GDB:

    gdb --args python3 ./main.py

Detener en la función de C:

    break to_int_plus_one

Entrar en las funciones:

    step [s]

Ejecuta la siguiente línea sin entrar en funciones.

    next [n]

Continúa la ejecución.

    continue [c]

Imprime el valor de una variable:

    print value_float
    print $eax
    print $rax
