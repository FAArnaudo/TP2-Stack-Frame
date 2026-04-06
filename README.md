# TP2-Stack-Frame

Trabajo práctico de Sistemas de Computación sobre consumo de la API del Banco Mundial, integración Python/C/Assembler y análisis de stack frame.

## Grupo

- *Ataque x86*

## Integrantes

- *Arnaudo, Federico Andres*
- *Bonfils, Matías Gabriel*
- *Perotti, Franco José*

## Descripción

`main.py` consulta la API del Banco Mundial para obtener valores del índice GINI entre 2011 y 2020 a partir de un codigo de pais como `ar` o `arg`.

Cada valor no nulo se envía a una librería compartida escrita en C y assembler:

- `src/converter.c` actúa como capa intermedia
- `src/to_int.s` convierte `float` a `int`
- `src/plus_one.s` suma `1` al valor entero

El programa muestra una tabla con los valores originales y convertidos, y además genera un gráfico del índice GINI por año usando `matplotlib`.

Los artefactos compilados se generan en `build/`.

## Estructura del repositorio

```text
.
├── README.md
├── Makefile
├── main.py
├── src/
│   ├── converter.c
│   ├── to_int.s
│   └── plus_one.s
├── build/
└── docs/
    ├── verification.md
    └── screenshots/
```

## Compilación

Compilación normal:

```bash
make
```

Compilación con símbolos de depuración para GDB:

```bash
make debug
```

## Ejecución

Dependencias de Python utilizadas en tiempo de ejecución:

- `requests`
- `matplotlib`

Ejecutar desde la raíz del repositorio:

```bash
python3 ./main.py
```

o bien:

```bash
make run
```

Después de imprimir la tabla, el programa abre una ventana con el gráfico de los valores GINI ordenados por año.

## GDB

Compilar con símbolos de depuración:

```bash
make debug
```

Iniciar GDB:

```bash
gdb --args python3 ./main.py
```

Al iniciar GDB, el proceso depurado es `python3` y la librería compartida todavía no fue cargada. Por eso, en ese momento, los símbolos `to_int_plus_one`, `to_int` y `plus_one` aún no están disponibles para GDB.

Como `ctypes` carga `build/to_int_plus_one.so` recién durante la ejecución del programa, conviene usar breakpoints pendientes. De ese modo, GDB acepta el breakpoint aunque la función todavía no sea conocida y lo resuelve automáticamente cuando la librería se carga en memoria.

```gdb
set breakpoint pending on
break to_int_plus_one
break to_int
break plus_one
run
```

## Verification Report

El informe de compilación, ejecución y depuración se encuentra en [`docs/verification.md`](docs/verification.md).
