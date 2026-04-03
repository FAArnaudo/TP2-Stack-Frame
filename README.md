# TP2-Stack-Frame
Este el repositorio del trabajo práctico N° 2 de la materia de Sistemas de Computación

## Grupo
- **Ataque x86**

## Integrantes
-  *Arnaudo, Federico Andres*
- 
- 

# Script de Python - main.py

Este programa en Python consulta la API del Banco Mundial para obtener valores del índice GINI de un país ingresado por el usuario (entre 2011 y 2020). 

Luego, utiliza la librería `ctypes` para cargar una biblioteca compartida escrita en C (`toIntPlusOne.so`) y llamar a una función que convierte cada valor flotante en entero y le suma uno. 

Finalmente, muestra tanto el valor original como el valor transformado, repitiendo el proceso hasta que el usuario decida finalizar.


# Comandos utilizados:

```gcc -shared -W -o toIntPlusOne.so toIntPluesOne.c```

Usa el compilador GCC (GNU Compiler Collection) para crear una biblioteca compartida.

- -shared: Esto nos crea un fichero shared object llamado toIntPluesOne.so.
- -W: Activa warnings (advertencias) del compilador.
- -o: Define el nombre del archivo .so de salida.

Compila el archivo C y genera una librería compartida (.so) llamada toIntPlusOne.so, que luego puede ser usada por el programa **main.py**.

```python3 ./main.py```

Para ejecutar el script de python