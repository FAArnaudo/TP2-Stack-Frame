# TP2-Stack-Frame
Este es el repositorio del trabajo práctico N° 2 de la materia de Sistemas de Computación.

## Grupo
- *Ataque x86*

## Integrantes
- *Arnaudo, Federico Andres*
- *Perotti, Franco José*

# Script de Python - main.py

Este programa en Python consulta la API del Banco Mundial para obtener valores del indice GINI de un codigo de pais ingresado por el usuario (por ejemplo, `ar` o `arg`) entre 2011 y 2020.

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
    A[Usuario ingresa un codigo de pais] --> B[main.py]
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

    U->>P: Ingresa codigo de pais
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

# Comandos utilizados

Para compilar el proyecto:

```make```

Este comando:

- ensambla `to_int.s` y `plus_one.s`
- compila `converter.c`
- genera la biblioteca compartida `to_int_plus_one.so`

Para ejecutar el script de Python:

```python3 ./main.py```

o bien:

```make run```

Nota: antes de ejecutar `main.py`, debe existir `to_int_plus_one.so`.


## Convención de llamada

Compilación normal del proyecto:

```as -o to_int.o to_int.s```

```as -o plus_one.o plus_one.s```

```gcc -Wall -fPIC -c -o converter.o converter.c```

```gcc -shared -o to_int_plus_one.so converter.o to_int.o plus_one.o```

Si se quiere depurar con GDB con símbolos de depuración, conviene recompilar manualmente con:

```as --64 -g -o to_int.o to_int.s```

```as --64 -g -o plus_one.o plus_one.s```

```gcc -g -O0 -fPIC -c -o converter.o converter.c```

```gcc -shared -o to_int_plus_one.so converter.o to_int.o plus_one.o```

## GDB

Antes de usar GDB, conviene recompilar la biblioteca con símbolos de depuración usando los comandos de la sección anterior.

Iniciar la ejecución con GDB:

    gdb --args python3 ./main.py

Como la biblioteca compartida se carga dinámicamente desde Python, antes de definir breakpoints conviene ejecutar:

    set breakpoint pending on

Detener en la función de C:

    break to_int_plus_one

También se puede detener en las rutinas ASM:

    break to_int
    break plus_one

Ejecutar el programa:

    run

Durante la ejecución, ingresar un código de país válido, por ejemplo `ar`, para que Python invoque la biblioteca compartida y se activen los breakpoints pendientes.

Entrar en las funciones:

    step [s]

Para avanzar instrucción por instrucción en ASM:

    stepi [si]

Ejecuta la siguiente línea sin entrar en funciones.

    next [n]

Para avanzar sin entrar en la siguiente instrucción ASM:

    nexti [ni]

Continúa la ejecución.

    continue [c]

Inspección útil en la función de C (`to_int_plus_one`):

    print numb_float
    next
    print result
    print $eax
    print $rax
    info registers rax rbp rsp
    x/4xg $rsp

Nota: `print result` funciona en el contexto de `to_int_plus_one` luego de avanzar una línea con `next`. En `to_int` y `plus_one` conviene inspeccionar registros y stack con `info registers` y `x/... $rsp`.
